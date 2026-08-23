import { NextRequest, NextResponse } from 'next/server';

export async function GET(request: NextRequest) {
  const token = request.nextUrl.searchParams.get('token');
  const appUrl = process.env.NEXT_PUBLIC_SITE_URL || 'https://www.theclinixai.com';

  // Verification tokens must be validated server-side against the store used by
  // the request endpoint. This route intentionally does not mark an email as
  // verified from a browser-only value.
  if (!token) {
    return NextResponse.redirect(`${appUrl}/apply?verification=invalid`);
  }

  // The token validation/persistence is delegated to the configured verification
  // store. Until a persistent store is configured, never claim verification.
  return NextResponse.redirect(`${appUrl}/apply?verification=invalid`);
}
