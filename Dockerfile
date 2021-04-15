FROM kitware/paraview:pv-v5.8.0-osmesa-py3

LABEL org.label-schema.name="vtk-offscreen-rendering-server" \
    org.label-schema.schema-version="0.0.1"
ENV LANG=en_US.utf8

USER root
RUN pip3 install flask
WORKDIR /data
ENTRYPOINT ["python", "/data/rendering_server/main.py"]

