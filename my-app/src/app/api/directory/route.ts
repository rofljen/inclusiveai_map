import { NextResponse } from 'next/server';
import postgres from 'postgres';

export async function GET() {
  try {
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
        ln.lang_name as language,
        ln.wer_asr as "werAsr",
        ln.bleu_nmt as "bleuNmt",
        ln.chrf_nmt as "chrfNmt",
        ln.has_tts as "hasTts"
      FROM language_new ln
      ORDER BY ln.lang_name ASC;
    `;

    return NextResponse.json(result);
  } catch (error) {
    console.error('Error:', error);
    return NextResponse.json({ error: 'Internal Server Error' }, { status: 500 });
  }
}
