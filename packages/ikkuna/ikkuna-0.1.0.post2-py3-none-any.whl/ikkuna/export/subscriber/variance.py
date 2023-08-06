from ikkuna.export.subscriber import PlotSubscriber, Subscription
from ikkuna.export.messages import get_default_bus


class VarianceSubscriber(PlotSubscriber):
    '''A :class:`~ikkuna.export.subscriber.Subscriber` which computes the
    variance of quantity for the current batch.
    '''

    def __init__(self, kind, message_bus=get_default_bus(), tag='default', subsample=1, ylims=None,
                 backend='tb'):

        if not isinstance(kind, str):
            raise ValueError('VarianceSubscriber only accepts 1 kind')

        title        = f'{kind}_variance'
        ylabel       = 'σ^2'
        xlabel       = 'Train step'
        subscription = Subscription(self, [kind], tag=tag, subsample=subsample)
        super().__init__([subscription], message_bus,
                         {'title': title,
                          'ylabel': ylabel,
                          'ylims': ylims,
                          'xlabel': xlabel},
                         backend=backend)

        self._add_publication(f'{kind}_variance', type='DATA')

    def compute(self, message):
        '''Compute the variance of a quantity. A :class:`~ikkuna.export.messages.ModuleMessage`
        with the identifier ``{kind}_variance`` is published. '''

        module, module_name = message.key
        data                = message.data
        var                 = data.var()
        self._backend.add_data(module_name, var, message.global_step)

        kind = f'{message.kind}_variance'
        self.message_bus.publish_module_message(message.global_step,
                                                message.train_step,
                                                message.epoch, kind,
                                                message.key, var)
