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
      WHERE id = ${parseInt(id)}
      LIMIT 1;
    `;

    await sql.end();
    return NextResponse.json(result[0]);
  } catch (error) {
    console.error('Error fetching language:', error);
    return NextResponse.json(
      { error: 'Failed to fetch language details' },
      { status: 500 }
    );
  }
}
