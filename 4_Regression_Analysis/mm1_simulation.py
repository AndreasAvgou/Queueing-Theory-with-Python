import numpy as np

def simulate_mm1_one_run(lmbda, mu, max_time=1000.0, warmup_time=0.0, rng=None):
    """
    Simulates an M/M/1 queue for given lambda and mu.
    
    Args:
        lmbda (float): Arrival rate.
        mu (float): Service rate.
        max_time (float): Total simulation time.
        warmup_time (float): Time period to exclude from statistics collection.
        rng (numpy.random.Generator, optional): Random number generator instance.

    Returns:
        int: Maximum queue length observed (nq_max) excluding the customer in service.
    """
    if rng is None:
        rng = np.random.default_rng()

    rho = lmbda / mu
    if rho >= 1.0:
        raise ValueError("For M/M/1, rho = lambda/mu must be < 1.")

    # Initialization
    t = 0.0                          # Current time
    queue_length = 0                 # Customers in queue (excluding service)
    server_busy = False              # Is server busy?
    t_next_arrival = rng.exponential(1.0 / lmbda)  # Time of next arrival
    t_next_departure = np.inf        # No departure scheduled if idle

    nq_max = 0

    while t < max_time:
        # Select next event (arrival or departure)
        if t_next_arrival <= t_next_departure:
            # Event: Arrival
            t = t_next_arrival
            # Schedule next arrival
            t_next_arrival = t + rng.exponential(1.0 / lmbda)

            if not server_busy:
                # Server idle -> start service immediately
                server_busy = True
                t_next_departure = t + rng.exponential(1.0 / mu)
            else:
                # Server busy -> join queue
                queue_length += 1
                # Update max queue length ONLY after warmup
                if t >= warmup_time and queue_length > nq_max:
                    nq_max = queue_length

        else:
            # Event: Departure (Service completion)
            t = t_next_departure
            if queue_length > 0:
                # Customer from queue starts service
                queue_length -= 1
                t_next_departure = t + rng.exponential(1.0 / mu)
                # (nq_max is not updated here, queue decreases)
            else:
                # Queue empty -> server becomes idle
                server_busy = False
                t_next_departure = np.inf

    return nq_max