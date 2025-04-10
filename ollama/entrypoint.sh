#!/bin/sh
set -e

OLLAMA_MODEL="${OLLAMA_MODEL}"

echo "Starting ollama serve..."
ollama serve &

sleep 3
echo "Running model: $OLLAMA_MODEL"
ollama run "$OLLAMA_MODEL"

echo "Checking Qdrant collection: ${QDRANT_COLLECTION_NAME}"

EXISTS=$(curl -s -o /dev/null -w "%{http_code}" "http://${QDRANT_HOST:-localhost}:6333/collections/${QDRANT_COLLECTION_NAME}")

if [ "$EXISTS" -eq 200 ]; then
  echo "Collection '${QDRANT_COLLECTION_NAME}' already exists. Skipping creation."
else
  echo "Creating collection: ${QDRANT_COLLECTION_NAME}"
  curl -s -X PUT "http://${QDRANT_HOST:-localhost}:6333/collections/${QDRANT_COLLECTION_NAME}" \
    -H "Content-Type: application/json" \
    -d '{
      "vectors": {
        "size": '"${QDRANT_VECTOR_SIZE:-384}"',
        "distance": "Cosine"
      }
    }'
  echo "Collection '${QDRANT_COLLECTION_NAME}' created."
fi

wait