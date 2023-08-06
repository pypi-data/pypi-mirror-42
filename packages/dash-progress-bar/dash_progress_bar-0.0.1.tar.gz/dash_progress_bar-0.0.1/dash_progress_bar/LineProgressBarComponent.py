# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class LineProgressBarComponent(Component):
    """A LineProgressBarComponent component.
LineProgressBarComponent

Keyword arguments:
- id (string; optional): The ID used to identify this component in Dash callbacks
- strokeWidth (number; optional): The width of stroke, default 1, unit is percentage of SVG canvas size
- strokeColor (string; optional): The color of stroke, default #2db7f5
- trailWidth (number; optional): The width of trail stroke, default & unit are the same as strokeWidth
- trailColor (string; optional): The color of trail
- strokeLinecap (string; optional): the shape to be used at the end of progres bar, {'butt', 'square', 'round'}
default is round
- percent (optional): the percent of progress
- style (dict; optional): Style of the element"""
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, strokeWidth=Component.UNDEFINED, strokeColor=Component.UNDEFINED, trailWidth=Component.UNDEFINED, trailColor=Component.UNDEFINED, strokeLinecap=Component.UNDEFINED, percent=Component.UNDEFINED, style=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'strokeWidth', 'strokeColor', 'trailWidth', 'trailColor', 'strokeLinecap', 'percent', 'style']
        self._type = 'LineProgressBarComponent'
        self._namespace = 'dash_progress_bar'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'strokeWidth', 'strokeColor', 'trailWidth', 'trailColor', 'strokeLinecap', 'percent', 'style']
        self.available_wildcard_properties =            []

        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(LineProgressBarComponent, self).__init__(**args)
