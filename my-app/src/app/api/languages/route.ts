import { NextResponse } from 'next/server';
import { loadLanguageData } from '../db';

export async function GET() {
  try {
    const languages = await loadLanguageData();
    
    // Transform the data to match the expected format
    const transformedLanguages = languages.map(lang => ({
      ...lang,
      available_models: lang.available_models.filter(Boolean),
      connected_languages: Array.isArray(lang.connected_languages) 
        ? lang.connected_languages 
        : lang.connected_languages?.split(',') || [],
      connected_coords: Array.isArray(lang.connected_coords) 
        ? lang.connected_coords 
        : lang.connected_coords ? JSON.parse(lang.connected_coords) : []
    }));

    return NextResponse.json(transformedLanguages);
  } catch (error) {
    console.error('Error fetching languages:', error);
    return NextResponse.json(
      { error: 'Failed to fetch languages' },
      { status: 500 }
    );
  }
}
