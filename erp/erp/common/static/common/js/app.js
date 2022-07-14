// Disable hotkeys system
var codenerix_hotkeys = false;

var module = codenerix_builder(
    ['codenerixPublicContactControllers'],
    {
        'list0': [null, null, null],
        'formadd0': {
            'controller': 'codenerixPublicContactCtrl'
        },
    },
    [
        ['', '/add'],
        ['/', '/add'],
        [undefined, '/add'],
    ],
);
