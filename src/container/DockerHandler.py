import logging

from docker import DockerClient

from src.container.model.ContainerWrapper import ContainerWrapper
from src.container.model.Domain import DockerPublicNetwork
from src.render.OutputHandler import OutputHandler

logger = logging.getLogger(__name__)


class DockerHandler:
    client: DockerClient
    topology: DockerPublicNetwork

    def __init__(self, client: DockerClient, output_handler: OutputHandler):
        self.client = client
        self.output_handler = output_handler

    def init(self):
        self.refresh_container(event=None)

    def handle(self, event):
        action = event['Action']
        if action in ['start', 'stop', 'die']:
            self.refresh_container(event)

    def refresh_container(self, event):
        logger.debug("###### REFRESH START ############################")
        self.topology = DockerPublicNetwork()
        done: bool = False
        retries: int = 0
        while not done and retries < 5:
            try:
                containers = self.client.containers.list(all=True)
                for container in containers:
                    container_wrap = ContainerWrapper(container)
                    if container_wrap.is_running():
                        self.topology.add_container(container_wrap)
                        logger.debug("RUNNING: " + container_wrap.id())
                        if container_wrap.is_relevant():
                            logger.info(
                                "FOUND RELEVANT RUNNING CONTAINER '%s'(id:%s)",
                                container_wrap.name(),
                                container_wrap.id()
                            )
                        logger.debug(container_wrap.id())
                self.output_handler.run(self.topology)
                done = True
                logger.debug("###### REFRESH END ############################")
            except Exception as e:
                logger.warning("Exception %s", e, exc_info=True)
                retries += 1
