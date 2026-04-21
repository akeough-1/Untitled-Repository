import math

gamma = 1.4


def area_mach(M, gamma=1.4):
    """
    Isentropic area-Mach relation A/A*
    """
    term1 = 1.0 / M
    term2 = (2.0 / (gamma + 1.0)) * (1.0 + (gamma - 1.0) / 2.0 * M**2)
    exponent = (gamma + 1.0) / (2.0 * (gamma - 1.0))
    return term1 * term2**exponent


def pressure_ratio(M, gamma=1.4):
    """
    Isentropic stagnation-to-static pressure ratio p0/p
    """
    return (1.0 + (gamma - 1.0) / 2.0 * M**2) ** (gamma / (gamma - 1.0))


def normal_shock_M2(M1, gamma=1.4):
    """
    Downstream Mach number after a normal shock
    """
    numerator = 1.0 + (gamma - 1.0) / 2.0 * M1**2
    denominator = gamma * M1**2 - (gamma - 1.0) / 2.0
    return math.sqrt(numerator / denominator)


def normal_shock_p2_p1(M1, gamma=1.4):
    """
    Static pressure ratio across a normal shock: p2/p1
    """
    return 1.0 + (2.0 * gamma / (gamma + 1.0)) * (M1**2 - 1.0)


def normal_shock_p02_p01(M1, gamma=1.4):
    """
    Stagnation pressure ratio across a normal shock: p02/p01
    Computed from:
      p02/p01 = (p2/p1) * (p0_2/p2) / (p0_1/p1)
    """
    M2 = normal_shock_M2(M1, gamma)
    p2_p1 = normal_shock_p2_p1(M1, gamma)

    p01_p1 = pressure_ratio(M1, gamma)
    p02_p2 = pressure_ratio(M2, gamma)

    return p2_p1 * (p02_p2 / p01_p1)


def mach_from_area(area_ratio, supersonic=True, gamma=1.4, tol=1e-10, max_iter=200):
    """
    Solve A/A* = area_ratio for Mach number using bisection.
    Returns either the subsonic or supersonic branch.
    """
    if area_ratio < 1.0:
        raise ValueError("Area ratio A/A* must be >= 1.")

    if abs(area_ratio - 1.0) < tol:
        return 1.0

    if supersonic:
        low = 1.000001
        high = 20.0
    else:
        low = 1e-8
        high = 0.999999

    for _ in range(max_iter):
        mid = 0.5 * (low + high)
        f_mid = area_mach(mid, gamma) - area_ratio
        f_low = area_mach(low, gamma) - area_ratio

        if abs(f_mid) < tol:
            return mid

        if f_low * f_mid < 0:
            high = mid
        else:
            low = mid

    return 0.5 * (low + high)


def compute_exit_from_shock_area(A2_At, Ae_At, gamma=1.4):
    """
    For a guessed shock location A2/At:
      1) find M1 just before the shock from supersonic branch
      2) compute M2 after the shock
      3) find downstream A2/A*2
      4) get Ae/A*2
      5) solve for exit Mach on subsonic branch
      6) compute predicted p01/pe

    Returns:
      M1, M2, Me, predicted_p01_pe
    """
    if A2_At <= 1.0:
        raise ValueError("Shock area ratio A2/At must be > 1.")
    if A2_At >= Ae_At:
        raise ValueError("Shock area ratio A2/At must be < Ae/At.")

    # Upstream of shock: supersonic branch based on A2/At = A2/A*1, and A*1 = At
    M1 = mach_from_area(A2_At, supersonic=True, gamma=gamma)

    # Across shock
    M2 = normal_shock_M2(M1, gamma)
    p02_p01 = normal_shock_p02_p01(M1, gamma)

    # Downstream, the new critical area A*2 is different
    # Since A2/A*2 is based on downstream subsonic M2:
    A2_Astar2 = area_mach(M2, gamma)

    # Therefore:
    Ae_Astar2 = (Ae_At / A2_At) * A2_Astar2

    # Exit must be on subsonic branch after the normal shock
    Me = mach_from_area(Ae_Astar2, supersonic=False, gamma=gamma)

    # p01/pe = (p01/p02) * (p02/pe)
    p02_pe = pressure_ratio(Me, gamma)
    predicted_p01_pe = (1.0 / p02_p01) * p02_pe

    return M1, M2, Me, predicted_p01_pe


def secant_solve_shock_area(Ae_At, target_p01_pe, guess1, guess2,
                            gamma=1.4, tol=1e-8, max_iter=50):
    """
    Use secant iteration on shock location A2/At so that
    predicted (p01/pe) matches target_p01_pe.
    """
    def residual(A2_At):
        _, _, _, pred = compute_exit_from_shock_area(A2_At, Ae_At, gamma)
        return pred - target_p01_pe

    x0 = guess1
    x1 = guess2
    f0 = residual(x0)
    f1 = residual(x1)

    print("Iterating on shock location A2/At")
    print("-" * 72)
    print(f"{'iter':>4} {'A2/At':>14} {'residual':>18} {'Me(exit)':>14} {'p01/pe(calc)':>16}")

    for i in range(max_iter):
        M1, M2, Me, pred = compute_exit_from_shock_area(x1, Ae_At, gamma)
        print(f"{i:4d} {x1:14.8f} {f1:18.10e} {Me:14.8f} {pred:16.8f}")

        if abs(f1) < tol:
            return x1, M1, M2, Me, pred, i + 1

        if abs(f1 - f0) < 1e-14:
            raise RuntimeError("Secant method failed: denominator became too small.")

        x2 = x1 - f1 * (x1 - x0) / (f1 - f0)

        # Keep the next guess inside the nozzle
        if x2 <= 1.0:
            x2 = 1.000001
        elif x2 >= Ae_At:
            x2 = 0.999999 * Ae_At

        x0, f0 = x1, f1
        x1 = x2
        f1 = residual(x1)

    raise RuntimeError("Secant method did not converge within max_iter.")


if __name__ == "__main__":
    # ---------------- USER INPUTS ----------------
    Ae_At = 1.53               # nozzle exit-to-throat area ratio
    target_p01_pe = 1.0 / 0.75 # example: p01 = 1 atm, pe = 0.94 atm

    # Two initial guesses for shock location A2/At
    guess1 = 1.01
    guess2 = Ae_At-1e-14
    # --------------------------------------------

    try:
        A2_At, M1, M2, Me, pred, niter = secant_solve_shock_area(
            Ae_At=Ae_At,
            target_p01_pe=target_p01_pe,
            guess1=guess1,
            guess2=guess2,
            gamma=gamma
        )

        print("\nConverged solution")
        print("-" * 72)
        print(f"Iterations              = {niter}")
        print(f"Shock location A2/At    = {A2_At:.8f}")
        print(f"Mach before shock M1    = {M1:.8f}")
        print(f"Mach after shock M2     = {M2:.8f}")
        print(f"Exit Mach number Me     = {Me:.8f}")
        print(f"Computed p01/pe         = {pred:.8f}")
        print(f"Target p01/pe           = {target_p01_pe:.8f}")

    except Exception as e:
        print(f"Error: {e}")