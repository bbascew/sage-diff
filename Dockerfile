FROM condaforge/miniforge3:latest

WORKDIR /workspace

RUN conda install -y -c conda-forge sage pytest && conda clean -afy

COPY pyproject.toml ./
COPY src ./src
COPY tests ./tests

RUN pip install -e .

CMD ["pytest"]
