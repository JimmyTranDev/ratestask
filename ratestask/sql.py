GET_RATES_SQL = """
    WITH RECURSIVE sub_regions AS (
        SELECT parent_slug, slug FROM regions
        WHERE parent_slug IS NOT NULL
        UNION ALL
        SELECT s.parent_slug, r.slug
        FROM sub_regions as s
        INNER JOIN regions AS r ON s.slug = r.parent_slug
    ),
    ports_prices AS (
        SELECT prices.*,
                orig_ports.parent_slug AS orig_slug,
                dest_ports.parent_slug AS dest_slug
        FROM prices
        INNER JOIN ports AS orig_ports
            ON prices.orig_code = orig_ports.code
        INNER JOIN ports AS dest_ports
            ON prices.dest_code = dest_ports.code
    )
    SELECT 
        day, 
        (CASE WHEN count(*) >= 3 THEN AVG(price) ELSE NULL END)
    FROM ports_prices
    WHERE 
        day >= %(date_from)s AND 
        day <= %(date_to)s AND 
        (
            orig_code = %(origin)s OR
            orig_slug = %(origin)s OR
            orig_slug IN (
                SELECT slug
                FROM sub_regions
                WHERE parent_slug = %(origin)s
            )
        ) AND
        (
            dest_code = %(destination)s OR
            dest_slug = %(destination)s OR
            dest_slug IN (
                SELECT slug
                FROM sub_regions
                WHERE parent_slug = %(destination)s
            )
        )
    GROUP BY day
    ORDER BY day
"""
