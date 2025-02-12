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
        ln.id,
        ln.lang_name as name,
        ST_Y(ln.coordinates::geometry) as latitude,
        ST_X(ln.coordinates::geometry) as longitude,
        lf.name as family_name,
        ls.name as subfamily_name,
        array_remove(ARRAY[
          CASE WHEN ln.asr THEN 'ASR' ELSE NULL END,
          CASE WHEN ln.nmt THEN 'NMT' ELSE NULL END,
          CASE WHEN ln.tts THEN 'TTS' ELSE NULL END
        ], NULL) as available_models,
        (
          SELECT COUNT(*)
          FROM nmt_pairs_source nps
          WHERE source_lang_id = ln.id OR target_lang_id = ln.id
        ) as nmt_pair_count
      FROM language_new ln
      LEFT JOIN language_family lf ON ln.lang_fam_id = lf.id
      LEFT JOIN language_subfamily ls ON ln.lang_sub_id = ls.id
      WHERE lf.id = ${parseInt(decodedName)}
      ORDER BY ln.lang_name ASC;
    `;

    await sql.end();
    return NextResponse.json(result);
  } catch (error) {
    console.error('Error fetching languages by family:', error);
    return NextResponse.json(
      { error: 'Failed to fetch languages by family' },
      { status: 500 }
    );
  }
}
