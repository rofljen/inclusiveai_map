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
        ln.iso_code,
        ln.glottocode,
        lf.name as family_name,
        lf.id as family_id,
        ls.name as subfamily_name,
        ls.id as subfamily_id,
        ln.asr,
        ln.nmt,
        ln.tts,
        ln.asr_url,
        ln.nmt_url,
        ln.tts_url,
        ST_Y(ln.coordinates::geometry) as latitude,
        ST_X(ln.coordinates::geometry) as longitude,
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
      WHERE ln.id = ${parseInt(id)}
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
