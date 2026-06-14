import { globals } from "@/stores/global";
export const Query = async (config={}) => {
  const { path, method = 'GET', body, headers = {} } = config;
  const response = await fetch(`${globals.apiUrl}/${path}`, {
    method,
    headers: {
      'Content-Type': 'application/json',
      ...headers,
    },
    body: method === 'GET' ? null : JSON.stringify(body)
  });
  const data = await response.json();
  if (response.ok) {
    return data;
  } else {
    throw Object.assign(new Error(), { error: data.error, code: response.status });
  }
}
