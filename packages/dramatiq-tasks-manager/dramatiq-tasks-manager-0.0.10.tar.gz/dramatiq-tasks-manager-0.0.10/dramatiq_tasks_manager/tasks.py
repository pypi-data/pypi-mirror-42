import dramatiq


@dramatiq.actor(max_retries=0, max_age=3600000, time_limit=6000, store_results=True, result_ttl=6000000)
def test_actor():
    return 'Success'
