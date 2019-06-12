// Change YOUR_API_KEY_HERE to your apiKey
const url = "http://192.168.43.51:5000/api/v1/user/40/suggestedPaths";

export async function getNews() {
  let result = await fetch(url).then(response => response.json());
  return result;
}
