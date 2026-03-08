"""Chunk transcript segments into overlapping text windows."""


def chunk_transcript(
    transcript: list[dict],
    window_seconds: float = 60.0,
    overlap_seconds: float = 10.0,
) -> list[dict]:
    """Split a transcript into overlapping text chunks.

    Parameters
    ----------
    transcript : list of dicts with keys ``text``, ``start``, ``duration``
    window_seconds : target duration (seconds) for each chunk
    overlap_seconds : how far to "rewind" when starting the next chunk

    Returns
    -------
    list of dicts with keys ``text``, ``start_time``, ``end_time``
    """
    if not transcript:
        return []

    chunks: list[dict] = []
    idx = 0
    n = len(transcript)

    while idx < n:
        # Accumulate segments until we fill the window
        texts: list[str] = []
        start_time = transcript[idx]["start"]
        window_end = start_time + window_seconds
        j = idx

        while j < n:
            seg = transcript[j]
            seg_start = seg["start"]
            # Stop if this segment starts beyond the window
            if seg_start >= window_end and texts:
                break
            texts.append(seg["text"])
            j += 1

        # end_time = start of last included segment + its duration
        last_seg = transcript[j - 1]
        end_time = last_seg["start"] + last_seg.get("duration", 0.0)

        chunk_text = " ".join(texts).strip()
        if chunk_text:
            chunks.append({
                "text": chunk_text,
                "start_time": start_time,
                "end_time": end_time,
            })

        # Advance: walk forward past the overlap point
        if j >= n:
            break

        step_time = start_time + window_seconds - overlap_seconds
        next_idx = idx
        while next_idx < n and transcript[next_idx]["start"] < step_time:
            next_idx += 1

        # Ensure we always advance at least one segment
        if next_idx <= idx:
            next_idx = idx + 1

        idx = next_idx

    return chunks
