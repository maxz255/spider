class Mixin(object):
    def __repr__(self):
        class_name = self.__class__.__name__
        properties = ('{} = {}'.format(k, v) for k, v in self.__dict__.items())
        return '\n<{}:\n  {}\n>'.format(class_name, '\n  '.join(properties))
