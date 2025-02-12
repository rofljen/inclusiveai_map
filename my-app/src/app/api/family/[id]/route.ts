import { NextResponse } from 'next/server';
import postgres from 'postgres';

export async function GET(
  request: Request,
  { params }: { params: Promise<{ id: string }> }
) {
  try {
    const { id } = await params;

    const sql = postgres({
      host: process.env.PGHOST,
      port: parseInt(process.env.PGPORT || '5432'),
      database: process.env.PGDATABASE,
      username: process.env.PGUSER,
      password: process.env.PGPASSWORD,
    });

    const result = await sql`
      SELECT 
        ln.id,
        ln.lang_name as name,
        lf.name as family_name
      FROM language_new ln
      LEFT JOIN language_family lf ON ln.lang_fam_id = lf.id
      WHERE ln.lang_fam_id = ${parseInt(id)}
      ORDER BY ln.lang_name;
    `;

    return NextResponse.json(result);
  } catch (error) {
    console.error('Error:', error);
    return NextResponse.json(
      { error: 'Failed to fetch family languages' },
      { status: 500 }
    );
  }
}
