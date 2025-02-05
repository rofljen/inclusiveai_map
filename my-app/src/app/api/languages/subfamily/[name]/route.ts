import { NextResponse } from 'next/server';
import postgres from 'postgres';

export async function GET(
  request: Request,
  { params }: { params: Promise<{ name: string }> }
) {
  try {
    const { name } = await params;
    const decodedName = decodeURIComponent(name);

    const sql = postgres({
      host: process.env.PGHOST,
      port: parseInt(process.env.PGPORT || '5432'),
      database: process.env.PGDATABASE,
      username: process.env.PGUSER,
      password: process.env.PGPASSWORD,
    });

    const result = await sql`
      SELECT 
        id,
        lang_name as name,
        iso_639_3_code as iso_code,
        latitude,
        longitude,
        family_name,
        subfamily_name,
        glotto_code,
        ARRAY(
          SELECT DISTINCT model_type::text
          FROM language_models
          WHERE language_id = language_new.id
        ) as available_models,
        (
          SELECT COUNT(*)
          FROM nmt_pairs_source nps
          WHERE source_lang_id = language_new.id OR target_lang_id = language_new.id
        ) as nmt_pair_count
      FROM language_new
      WHERE subfamily_name = ${decodedName}
      ORDER BY lang_name ASC;
    `;

    await sql.end();
    return NextResponse.json(result);
  } catch (error) {
    console.error('Error fetching languages by subfamily:', error);
    return NextResponse.json(
      { error: 'Failed to fetch languages by subfamily' },
      { status: 500 }
    );
  }
}
