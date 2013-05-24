DROP TABLE knows;
DROP FUNCTION select_connected_users(owner integer);
DROP TABLE curs_user;

create table curs_user
(
id SERIAL PRIMARY KEY,
email VARCHAR(255) UNIQUE,
name VARCHAR(255)
);

create table knows
(
id SERIAL PRIMARY KEY,
owner_id int references curs_user(id),
recipient_id int references curs_user(id)
);


CREATE FUNCTION select_connected_users(owner integer) returns setof varchar(255) as $$
BEGIN
    RETURN QUERY(SELECT curs_user.email FROM curs_user, knows WHERE owner_id=owner and recipient_id=curs_user.id);
END;
$$ LANGUAGE plpgsql;


