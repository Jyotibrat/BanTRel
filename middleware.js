export const config = {
  matcher: '/api/:path*',
};

export default function middleware(request) {
  const url = new URL(request.url);
  let backendUrl = process.env.BACKEND_URL;

  if (!backendUrl) {
    return new Response(JSON.stringify({ error: "BACKEND_URL is not set in Vercel environment variables." }), { 
      status: 500,
      headers: { "Content-Type": "application/json" }
    });
  }

  // Ensure the backend URL has a protocol
  if (!backendUrl.startsWith('http')) {
    backendUrl = 'https://' + backendUrl;
  }

  // Extract the path after /api and append to the backend URL
  const path = url.pathname.replace(/^\/api/, '');
  const targetUrl = new URL(path + url.search, backendUrl);

  // Return a rewrite directive to Vercel's edge network
  // This causes Vercel to fetch the target URL secretly and return the response to the client
  return new Response(null, {
    headers: {
      'x-middleware-rewrite': targetUrl.toString(),
    },
  });
}
