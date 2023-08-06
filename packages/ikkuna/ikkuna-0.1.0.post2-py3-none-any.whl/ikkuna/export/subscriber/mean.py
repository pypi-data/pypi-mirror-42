from ikkuna.export.subscriber import PlotSubscriber, Subscription
from ikkuna.export.messages import get_default_bus


class MeanSubscriber(PlotSubscriber):

    def __init__(self, kind, message_bus=get_default_bus(), tag='default', subsample=1, ylims=None,
                 backend='tb'):

        if not isinstance(kind, str):
            raise ValueError('MeanSubscriber only accepts 1 kind')

        title        = f'{kind}_mean'
        ylabel       = 'Mean'
        xlabel       = 'Train step'
        subscription = Subscription(self, [kind], tag=tag, subsample=subsample)
        super().__init__([subscription], message_bus,
                         {'title': title,
                          'ylabel': ylabel,
                          'ylims': ylims,
                          'xlabel': xlabel},
                         backend=backend)
        self._add_publication(f'{kind}_mean', type='DATA')

    def compute(self, message):
        '''Compute the average of a quantity. A :class:`~ikkuna.export.messages.ModuleMessage`
        with the identifier ``{kind}_mean`` is published. '''

        module, module_name  = message.key

        data = message.data
        mean = data.mean()
        self._backend.add_data(module_name, mean, message.global_step)

        kind = f'{message.kind}_mean'
        self.message_bus.publish_module_message(message.global_step,
                                                message.train_step,
                                                message.epoch, kind,
                                                message.key, mean)
