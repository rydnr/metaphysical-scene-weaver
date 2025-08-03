# Project Clarifications - Metaphysical Scene Weaver

## API & External Services

### Semantest API
**Status**: No credentials or documentation provided yet

**Assumptions for Development**:
- REST API with JSON payloads
- Authentication via API key in header
- Endpoint structure: `POST /api/generate`
- Rate limits: Assume 60 requests/minute
- Response: JSON with image URL

**Development Approach**:
1. Build with mock API for testing
2. Use environment variable: `SEMANTEST_API_KEY`
3. Create adapter pattern for easy swap
4. Document assumed API contract

### Prompt Format (Iris's Discovery)
Standard structure for all prompts:
```
[Style] + [Composition] + [Subject] + [Emotion] + [Effects] + [Quality]
```

Example:
```
"Graphic novel style, close-up composition, philosophical seeker contemplating existence, 
melancholic yet hopeful mood, ethereal lighting effects, high quality detailed rendering"
```

## Technical Decisions

### Metadata Format
**Decision**: JSON format for all metadata files

**Rationale**:
- Already in dependencies
- Human readable
- Supports complex structures
- Easy validation with Pydantic

**Standard Fields**:
```json
{
  "scene_id": "string",
  "timestamp": "ISO 8601",
  "prompt_version": "semver",
  "philosophy_concepts": ["array", "of", "concepts"],
  "emotion_state": "string",
  "visual_complexity": "low|medium|high",
  "narrator_included": boolean,
  "dependencies": {
    "previous_scene": "id",
    "next_scene": "id"
  }
}
```

### File Naming Conventions
- Scenes: `001.txt`, `002.txt` (zero-padded)
- Metadata: `001_metadata.json`
- Narrator: `001_narrator.txt`
- Transitions: `001-002_transition.txt`

### Testing Strategy
1. **Unit Tests**: Core logic without external dependencies
2. **Mock API Tests**: Semantest integration with mocked responses
3. **Integration Tests**: Full pipeline with test data
4. **E2E Tests**: Complete workflow (when API available)

## Environment Variables
```bash
SEMANTEST_API_KEY=placeholder_until_provided
SEMANTEST_API_URL=https://api.semantest.com/v1  # assumed
MSW_OUTPUT_DIR=./output
MSW_LOG_LEVEL=INFO
```

## Pending Clarifications from Owner

1. **Semantest API Credentials**: Need actual API key and documentation
2. **Output Preferences**: Any specific image format requirements?
3. **Batch Processing**: Should we process all scenes or allow selective generation?
4. **Error Handling**: How to handle failed image generations?
5. **Versioning**: Should we support multiple prompt versions per scene?

## Team Coordination Points

### Interfaces to Define
1. **Parser → Narrator Engine**: Entry format with narrator points
2. **Narrator → Prompt Generator**: Enhanced text format
3. **Folder Generator → API Client**: Manifest structure
4. **API Client → Storage**: Image organization

### Shared Libraries Needed
1. **Common Types**: `src/types/common.py`
2. **Validators**: `src/validators/`
3. **Utils**: `src/utils/io_helpers.py`

---
*Last Updated: Sprint 1, Day 1*
*Next Review: 2 PM Team Sync*