import pandas as pd

def ensure_records(data, headers: list | None = None):
    """
    Garantir que o resultado seja uma lista de dicionários (records).
    - aceita: pandas.DataFrame, list[dict], list[list|tuple], numpy.ndarray
    - se receber lista de listas/tuplas requer `headers` (nomes das colunas) para zipar.
    Retorna: list[dict]
    """
    import pandas as pd
    try:
        import numpy as np
    except Exception:
        np = None

    if data is None:
        return []

    # DataFrame -> records
    if isinstance(data, pd.DataFrame):
        return data.to_dict(orient="records")

    # numpy array -> DataFrame -> records
    if np is not None and isinstance(data, np.ndarray):
        df = pd.DataFrame(data, columns=headers) if headers else pd.DataFrame(data)
        return df.to_dict(orient="records")

    # list handling
    if isinstance(data, list):
        if len(data) == 0:
            return []
        first = data[0]
        # list of dicts -> assume already records
        if isinstance(first, dict):
            return data
        # list of lists/tuples -> need headers
        if isinstance(first, (list, tuple)):
            if headers is None:
                raise ValueError("ensure_records: 'headers' required for list of lists/tuples")
            return [dict(zip(headers, row)) for row in data]
        # list of scalars -> wrap into dict with single column if headers provided
        if headers and len(headers) == 1:
            return [{headers[0]: v} for v in data]
        # fallback: return as-is (list)
        return data

    # try to coerce other iterables via DataFrame
    try:
        df = pd.DataFrame(data)
        return df.to_dict(orient="records")
    except Exception:
        raise TypeError(f"ensure_records: tipo não suportado {type(data)}")