export async function sendJsonToBackend(data: object): Promise<number[][]> {
    try {
        const response = await fetch('http://127.0.0.1:5000/solve', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });
        console.log(data);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const result = await response.json();
        return result;
    } catch {
        return [];
    }
}