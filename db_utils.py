import os
import subprocess
import tempfile
import streamlit as st

def handle_backup_upload():
    """Handle the upload of a PostgreSQL database backup file."""
    uploaded_file = st.file_uploader("Choose a PostgreSQL backup file", type=['sql', 'dump'])

    if uploaded_file is not None:
        try:
            # Create a temporary file to store the upload
            with tempfile.NamedTemporaryFile(delete=False, suffix='.sql') as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                tmp_file_path = tmp_file.name

            # Add detailed logging
            st.write("Attempting to restore backup...")

            # First, try to check the backup file content
            st.write("Analyzing backup file contents...")
            with open(tmp_file_path, 'r') as f:
                backup_content = f.read()
                st.write(f"Backup file size: {len(backup_content)} bytes")

            # Construct psql command using environment variables
            env = os.environ.copy()
            db_params = {
                'host': os.getenv('PGHOST'),
                'port': os.getenv('PGPORT'),
                'user': os.getenv('PGUSER'),
                'password': os.getenv('PGPASSWORD'),
                'database': os.getenv('PGDATABASE')
            }
            env['PGPASSWORD'] = db_params['password']

            # Now perform the actual restore with verbose output
            st.write("Starting database restore...")

            result = subprocess.run(
                [
                    'psql',
                    '-h', db_params['host'],
                    '-p', db_params['port'],
                    '-U', db_params['user'],
                    '-d', db_params['database'],
                    '-v', 'ON_ERROR_STOP=1',
                    '-f', tmp_file_path
                ],
                env=env,
                capture_output=True,
                text=True
            )

            if result.returncode == 0:
                st.success("Database backup restored successfully!")
                # Verify the restoration
                verify_queries = [
                    """SELECT COUNT(*) as total_rows, 
                       COUNT(DISTINCT source_lang_id) as unique_sources,
                       COUNT(DISTINCT target_lang_id) as unique_targets
                    FROM nmt_pairs_source;"""
                ]

                st.write("Post-restore database state:")
                for query in verify_queries:
                    verify_result = subprocess.run(
                        ['psql',
                         '-h', db_params['host'],
                         '-p', db_params['port'],
                         '-U', db_params['user'],
                         '-d', db_params['database'],
                         '-c', query
                        ],
                        env=env,
                        capture_output=True,
                        text=True
                    )
                    st.code(verify_result.stdout)

            else:
                st.error("Error restoring backup. Details:")
                st.code(result.stderr)
                st.write("Command output:")
                st.code(result.stdout)

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            st.write("Full error details:", str(e))
        finally:
            # Clean up the temporary file
            if 'tmp_file_path' in locals():
                os.unlink(tmp_file_path)