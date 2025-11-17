import api from "../api";

export const streamGraph = (fileName, prompt = "", onMessage, onDone) => {
  if (!fileName) throw new Error("fileName is required for streaming graph.");

  // Build SSE URL safely
  const backendUrl = api.defaults.baseURL.replace(/\/$/, ""); // remove trailing slash
  const sseUrl = `${backendUrl}/graph_stream?file_name=${encodeURIComponent(fileName)}&prompt=${encodeURIComponent(prompt)}`;

  const evtSource = new EventSource(sseUrl);

  evtSource.onmessage = (event) => {
    try {
      const data = JSON.parse(event.data);

      if (data.done) {
        evtSource.close();        // ✅ close when stream ends
        onDone?.();
      } else if (data.node_name) {
        onMessage?.(data.node_name);
      }
    } catch (err) {
      console.error("Invalid SSE message:", err);
      evtSource.close();          // ✅ close on parse error too
    }
  };

  evtSource.onerror = (err) => {
    console.error("SSE connection closed unexpectedly", err);
    evtSource.close();            // ✅ stop auto-reconnect loop
    onDone?.();                   // optional: notify caller
  };

  return evtSource;
};
