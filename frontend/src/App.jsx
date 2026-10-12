import { useEffect, useState } from "react";

export default function App() {
  const [items, setItems] = useState([]);
  const [error, setError] = useState("");

  useEffect(() => {
    fetch("/api/items")
      .then((res) => {
        if (!res.ok) throw new Error("The server returned " + res.status);
        return res.json();
      })
      .then(setItems)
      .catch((err) =>
        setError("Could not load agenda items: " + err.message + ". Is the backend running on port 8000?")
      );
  }, []);

  return (
    <main>
      <h1>Agenda Alerts</h1>
      <p>Placeholder screen showing sample data from the backend.</p>
      {error && <p>{error}</p>}
      {items.map((item) => (
        <article key={item.id}>
          <h2>{item.title_original}</h2>
          <p>
            {item.body_name}, {item.meeting_date}
          </p>
          <p>{item.plain_summary}</p>
          <p>
            <a href={item.source.url}>Original agenda, page {item.source.page}</a>
          </p>
        </article>
      ))}
    </main>
  );
}
