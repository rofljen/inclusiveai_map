import postgres from 'postgres';

const sql = postgres({
  host: process.env.PGHOST,
  port: parseInt(process.env.PGPORT || '5432'),
  database: process.env.PGDATABASE,
  username: process.env.PGUSER,
  password: process.env.PGPASSWORD,
});

export async function query(text: string, params?: any[]) {
  const result = await sql.unsafe(text, params);
  return result;
}

export async function loadLanguageData() {
  const queryText = `
    WITH ordered_pairs AS (
      SELECT 
        l1.id as source_id,
        l2.lang_name as target_name,
        l2.id as target_id,
        ARRAY[
          ST_Y(l2.coordinates::geometry),
          ST_X(l2.coordinates::geometry)
        ]::float[] as target_coords,
        nps.chrf_plus,
        nps.spbleu_spm_200
      FROM language_new l1
      JOIN nmt_pairs_source nps ON l1.id = nps.source_lang_id OR l1.id = nps.target_lang_id
      JOIN language_new l2 ON 
        (nps.source_lang_id = l2.id OR nps.target_lang_id = l2.id) AND
        l2.id != l1.id
      WHERE l2.coordinates IS NOT NULL
        AND ST_IsValid(l2.coordinates::geometry)
      ORDER BY l2.lang_name
    ),
    lang_connections AS (
      SELECT 
        source_id as lang_id,
        array_agg(DISTINCT target_name) as connected_languages,
        array_agg(DISTINCT target_coords) FILTER (WHERE 
          target_coords[1] BETWEEN -90 AND 90
          AND target_coords[2] BETWEEN -180 AND 180
        ) as connected_coords,
        array_agg(DISTINCT target_id) as connected_lang_ids,
        array_agg(DISTINCT chrf_plus) as chrf_scores,
        array_agg(DISTINCT spbleu_spm_200) as bleu_scores
      FROM ordered_pairs
      GROUP BY source_id
    )
    SELECT 
      l.id,
      l.lang_name as name,
      l.iso_code,
      ST_Y(l.coordinates::geometry) as latitude,
      ST_X(l.coordinates::geometry) as longitude,
      ARRAY[
        CASE WHEN l.asr THEN 'ASR' END,
        CASE WHEN l.nmt THEN 'NMT' END,
        CASE WHEN l.tts THEN 'TTS' END
      ] as available_models,
      (SELECT COUNT(*)
       FROM nmt_pairs_source nps
       WHERE nps.source_lang_id = l.id OR nps.target_lang_id = l.id) as nmt_pair_count,
      COALESCE(lc.connected_languages, ARRAY[]::text[]) as connected_languages,
      COALESCE(lc.connected_coords, ARRAY[]::float[][]) as connected_coords,
      COALESCE(lc.connected_lang_ids, ARRAY[]::integer[]) as connected_lang_ids,
      COALESCE(lc.chrf_scores, ARRAY[]::float[]) as chrf_scores,
      COALESCE(lc.bleu_scores, ARRAY[]::float[]) as bleu_scores,
      CASE WHEN lc.lang_id IS NOT NULL THEN TRUE ELSE FALSE END as has_nmt_pair
    FROM language_new l
    LEFT JOIN lang_connections lc ON l.id = lc.lang_id
    WHERE l.coordinates IS NOT NULL
      AND ST_IsValid(l.coordinates::geometry)
      AND ST_X(l.coordinates::geometry) BETWEEN -180 AND 180
      AND ST_Y(l.coordinates::geometry) BETWEEN -90 AND 90
    ORDER BY l.lang_name
  `;

  const result = await sql.unsafe(queryText);
  return result;
}
