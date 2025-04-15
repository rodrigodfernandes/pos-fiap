BEGIN;
CREATE ROLE "fiap-embrapa" NOLOGIN;
CREATE ROLE "fiap-embrapa-admin" ROLE :"USER" IN ROLE "fiap-embrapa" NOINHERIT NOLOGIN;
CREATE ROLE "fiap-embrapa-dml" NOLOGIN;
CREATE ROLE "fiap-embrapa-ddl"  IN ROLE "fiap-embrapa-dml", "fiap-embrapa-admin" NOLOGIN;
CREATE ROLE "fiap-embrapa-ro" NOLOGIN;

CREATE ROLE "fiap-embrapa-app" LOGIN IN ROLE "fiap-embrapa-dml" password 'fiap-embrapa-app';
ALTER ROLE "fiap-embrapa-app" SET statement_timeout TO '33s';

CREATE ROLE "fiap-embrapa-migration" LOGIN IN ROLE "fiap-embrapa-ddl" password 'fiap-embrapa-migration';
ALTER ROLE "fiap-embrapa-migration" SET statement_timeout TO '33s';
ALTER ROLE "fiap-embrapa-migration" SET ROLE "fiap-embrapa";
COMMIT;

ALTER DATABASE "fiap-embrapa" OWNER TO "fiap-embrapa";

BEGIN;
REVOKE CREATE ON SCHEMA public FROM PUBLIC;
REVOKE CREATE ON DATABASE "fiap-embrapa" FROM PUBLIC;
GRANT CREATE ON SCHEMA public TO "fiap-embrapa";

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS pg_stat_statements;

SET ROLE "fiap-embrapa";
ALTER DEFAULT PRIVILEGES GRANT SELECT ON TABLES TO "fiap-embrapa-ro";
ALTER DEFAULT PRIVILEGES GRANT SELECT ON SEQUENCES TO "fiap-embrapa-ro";
ALTER DEFAULT PRIVILEGES GRANT SELECT,INSERT,UPDATE,DELETE ON TABLES TO "fiap-embrapa-dml";
ALTER DEFAULT PRIVILEGES GRANT USAGE, SELECT ON SEQUENCES TO "fiap-embrapa-dml";
ALTER DEFAULT PRIVILEGES GRANT EXECUTE ON FUNCTIONS TO "fiap-embrapa-dml";
ALTER DEFAULT PRIVILEGES GRANT USAGE ON SCHEMAS TO "fiap-embrapa-dml", "fiap-embrapa-ro";

GRANT SELECT ON ALL TABLES IN SCHEMA public TO "fiap-embrapa-ro";
GRANT SELECT ON ALL SEQUENCES IN SCHEMA public TO "fiap-embrapa-ro";
GRANT SELECT,INSERT,UPDATE,DELETE ON ALL TABLES IN SCHEMA public TO "fiap-embrapa-dml";
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO "fiap-embrapa-dml";
COMMIT;

CREATE SCHEMA IF NOT EXISTS fiap_embrapa;
ALTER SCHEMA fiap_embrapa OWNER TO "fiap-embrapa";

RESET ROLE;

ALTER DATABASE "fiap-embrapa" SET search_path = "fiap_embrapa", public;
