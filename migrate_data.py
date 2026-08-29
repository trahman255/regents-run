import json
from sqlalchemy import create_engine, MetaData, Table, select
from sqlalchemy.orm import sessionmaker

# 1. Source (Local PostgreSQL) & Target (Neon Cloud PostgreSQL)
LOCAL_DB_URL = "postgresql://postgres:jgsgeometry@localhost/geometry_app"
NEON_DB_URL = "postgresql://neondb_owner:npg_KcY52rksWyPv@ep-delicate-smoke-ayh5fdj7-pooler.c-5.us-east-2.aws.neon.tech/neondb?sslmode=require&channel_binding=require"

local_engine = create_engine(LOCAL_DB_URL)
neon_engine = create_engine(NEON_DB_URL)

local_meta = MetaData()
neon_meta = MetaData()

try:
    print("🔄 Connecting to local database and reading schema...")
    local_questions_table = Table("questions", local_meta, autoload_with=local_engine)
    neon_questions_table = Table("questions", neon_meta, autoload_with=neon_engine)

    with local_engine.connect() as local_conn:
        results = local_conn.execute(select(local_questions_table)).mappings().all()
        total_count = len(results)
        print(f"🚀 Found {total_count} questions in local PostgreSQL. Transferring to Neon...")

        if total_count > 0:
            records_to_insert = []
            for row in results:
                r_dict = dict(row)
                
                # Exclude local primary key so Neon generates its own sequence cleanly
                r_dict.pop("id", None)

                # Format options JSON safely
                if "options" in r_dict and isinstance(r_dict["options"], str):
                    try:
                        r_dict["options"] = json.loads(r_dict["options"])
                    except Exception:
                        r_dict["options"] = [r_dict["options"]]

                # Keep only fields that exist in the Neon table
                filtered_record = {
                    col.name: r_dict[col.name]
                    for col in neon_questions_table.columns
                    if col.name in r_dict and col.name != "id"
                }
                
                records_to_insert.append(filtered_record)

            with neon_engine.begin() as neon_conn:
                neon_conn.execute(neon_questions_table.insert(), records_to_insert)

            print(f"✅ Success! Transferred all {total_count} questions to Neon cloud database.")
        else:
            print("⚠️ No questions found to transfer.")

except Exception as e:
    print(f"❌ Error during migration: {e}")