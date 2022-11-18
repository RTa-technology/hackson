FROM mt08/rpi-jupyter-opencv3

ADD http://ci.tensorflow.org/view/Nightly/job/nightly-pi-python3/lastSuccessfulBuild/artifact/output-artifacts/tensorflow-1.4.0-cp34-none-any.whl .
RUN mv tensorflow-1.4.0-cp34-none-any.whl tensorflow-1.4.0-cp35-none-any.whl && sudo pip3 --no-cache-dir install tensorflow-1.4.0-cp35-none-any.whl && rm -rf tensorflow-1.4.0-cp35-none-any.whl
RUN sudo pip3 --no-cache-dir install requests

EXPOSE 6006
EXPOSE 8888
WORKDIR   "/notebooks"
ENTRYPOINT ["/sbin/tini", "--"]
CMD ["jupyter", "notebook", "--allow-root"]