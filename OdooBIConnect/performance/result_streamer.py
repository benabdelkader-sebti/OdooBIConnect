def stream_results(cr, batch_size=10000):

    while True:
        rows = cr.fetchmany(batch_size)
        if not rows:
            break
        for row in rows:
            yield row
