def test_health(client):
    r = client.get("/api/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"

def test_ingest_and_ask(client):
    r = client.post("/api/ingest")
    assert r.status_code == 200
    # Ask a deterministic question
    r2 = client.post("/api/ask", json={"query":"What is the refund window for small appliances?"})
    assert r2.status_code == 200
    data = r2.json()
    assert "citations" in data and len(data["citations"]) > 0
    assert "answer" in data and isinstance(data["answer"], str)

def test_metrics(client):
    r = client.get("/api/metrics")
    assert r.status_code == 200
    data = r.json()
    assert "total_docs" in data
    assert "total_chunks" in data
    assert "embedding_model" in data
    assert "llm_model" in data
    assert isinstance(data["total_docs"], int)
    assert isinstance(data["total_chunks"], int)

def test_ask_no_results(client):
    r = client.post("/api/ask", json={"query":"This is a nonsense query that should return nothing unique."})
    assert r.status_code == 200
    data = r.json()
    assert "citations" in data
    assert "chunks" in data
    assert isinstance(data["citations"], list)
    assert isinstance(data["chunks"], list)

def test_citation_chunk_expansion(client):
    r = client.post("/api/ingest")
    assert r.status_code == 200
    r2 = client.post("/api/ask", json={"query":"What’s the shipping SLA to East Malaysia for bulky items?"})
    assert r2.status_code == 200
    data = r2.json()
    assert "chunks" in data
    for chunk in data["chunks"]:
        assert "text" in chunk
        assert isinstance(chunk["text"], str)

def test_ask_invalid_input(client):
    # Missing 'query' field
    r = client.post("/api/ask", json={})
    assert r.status_code == 422
    # Invalid type for 'k'
    r2 = client.post("/api/ask", json={"query":123, "k":"not_a_number"})
    assert r2.status_code == 422

def test_ingest_invalid_method(client):
    r = client.get("/api/ingest")
    assert r.status_code == 405

def test_metrics_invalid_method(client):
    r = client.post("/api/metrics")
    assert r.status_code == 405

def test_health_invalid_method(client):
    r = client.post("/api/health")
    assert r.status_code == 405

def test_feedback_on_results(client):
    r = client.post("/api/ingest")
    assert r.status_code == 200
    r2 = client.post("/api/ask", json={"query":"Can a customer return a damaged blender after 20 days?"})
    assert r2.status_code == 200
    data = r2.json()
    feedback = []
    if "citations" in data and len(data["citations"]) > 0:
        feedback.append(f"Citations returned: {[c['title'] for c in data['citations']]}")
    else:
        feedback.append("No citations returned.")
    if "answer" in data and isinstance(data["answer"], str):
        feedback.append(f"Answer: {data['answer'][:80]}...")
    else:
        feedback.append("No answer returned.")
    if "chunks" in data and len(data["chunks"]) > 0:
        feedback.append(f"Chunks returned: {len(data['chunks'])}")
    else:
        feedback.append("No chunks returned.")
    print("\nTest Feedback:\n" + "\n".join(feedback))
