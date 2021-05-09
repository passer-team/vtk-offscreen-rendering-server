FROM kitware/paraview:pv-v5.8.0-osmesa-py3

LABEL org.label-schema.name="vtk-rendering-server" \
    org.label-schema.schema-version="0.0.1"
ENV LANG=en_US.utf8

USER root
RUN pip3 install flask
WORKDIR /app
COPY vtk_rendering_server /app/vtk_rendering_server
COPY script /app/script
ENTRYPOINT ["python", "/app/vtk_rendering_server/main.py"]

