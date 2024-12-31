import os
import subprocess
import tempfile
import streamlit as st

def handle_backup_upload():
    """Handle the upload of a PostgreSQL database backup file."""
    st.subheader("Database Backup Upload")
    
    uploaded_file = st.file_uploader("Choose a PostgreSQL backup file", type=['sql', 'dump'])
    
    if uploaded_file is not None:
        try:
            # Create a temporary file to store the upload
            with tempfile.NamedTemporaryFile(delete=False, suffix='.sql') as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                tmp_file_path = tmp_file.name
            
            # Construct the pg_restore command using environment variables
            db_url = os.getenv('DATABASE_URL')
            if not db_url:
                db_params = {
                    'host': os.getenv('PGHOST'),
                    'port': os.getenv('PGPORT'),
                    'user': os.getenv('PGUSER'),
                    'password': os.getenv('PGPASSWORD'),
                    'database': os.getenv('PGDATABASE')
                }
                
                # Use psql to restore the backup
                env = os.environ.copy()
                env['PGPASSWORD'] = db_params['password']
                
                result = subprocess.run(
                    [
                        'psql',
                        '-h', db_params['host'],
                        '-p', db_params['port'],
                        '-U', db_params['user'],
                        '-d', db_params['database'],
                        '-f', tmp_file_path
                    ],
                    env=env,
                    capture_output=True,
                    text=True
                )
                
                if result.returncode == 0:
                    st.success("Database backup restored successfully!")
                else:
                    st.error(f"Error restoring backup: {result.stderr}")
            
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
        finally:
            # Clean up the temporary file
            if 'tmp_file_path' in locals():
                os.unlink(tmp_file_path)
