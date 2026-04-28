def execute_streaming(env, sql, params):

    cr = env.cr
    cr.execute(sql, params)

    columns = [desc[0] for desc in cr.description]

    while True:
        rows = cr.fetchmany(10000)
        if not rows:
            break

        for row in rows:
            yield dict(zip(columns, row))
