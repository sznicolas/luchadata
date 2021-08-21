from collections import OrderedDict

class Lucha:
    def __init__(self, lucha_id, dna=None):
        self._id = self._set_id(lucha_id)
        self._realname = "Luchador #" + str(self._id)
        self._dna = self._set_dna(dna)
        self._attributes = OrderedDict()
        self._set_attributes()
        self._base_color = self._set_base_color()
        self._alt_color = self._set_alt_color()
        self._eyes = self._set_eye_color()
        self._skin = self._set_skin_color()

    def set_name(self, name):
        self._name = name

    def set_owner(self, owner):
        self._owner = owner

    def short_owner(self):
        if hasattr(self, '_owner'):
            return self._owner[:8] + ".." + self._owner[-6:]
        return ""

    def get_name(self):
        return self._name

    def fancy_name(self):
        if hasattr(self, '_name'):
            return f"-~-~-===( {self._name}  )===-~-~-"
        return ""

    def get_realname(self):
        return self._realname

    def _set_id(self, _id):
        if _id is None:
            return None
        if (_id < 1 or _id > 10_000):
            raise ValueError("Incorrect lucha_id: ", _id)
        return _id

    def _set_dna(self, dna):
        if len(str(dna)) < 12:
            raise ValueError("Incorrect dna < 12: ", dna)
        return str(dna)

    def _set_attributes(self):
        self._attributes['spirit'] = self._set_spirit(_nucleobase(self._dna, 0))
        self._attributes['cape'] = self._set_cape(_nucleobase(self._dna, 1))
        self._attributes['torso'] = self._set_torso(_nucleobase(self._dna, 2))
        self._attributes['arms'] = self._set_arms(_nucleobase(self._dna, 3))
        self._attributes['mask'] = self._set_mask(_nucleobase(self._dna, 4))
        self._attributes['mouth'] = self._set_mouth(_nucleobase(self._dna, 5))
        self._attributes['bottoms'] = self._set_bottoms(_nucleobase(self._dna, 6))
        self._attributes['boots'] = self._set_boots(_nucleobase(self._dna, 7))

    def get_attributes(self):
        return self._attributes

    def count_attributes(self):
        return sum(x is not None for x in list(self._attributes.values()))

    def _set_spirit(self, i):
        try:
            return list(spirit)[i]
        except(IndexError):
            return None

    def _set_cape(self, i):
        try:
            return list(cape)[i]
        except(IndexError):
            return None

    def _set_torso(self, i):
        try:
            return list(torso)[i]
        except(IndexError):
            return None

    def _set_arms(self, i):
        try:
            return list(arms)[i]
        except(IndexError):
            return None

    def _set_mask(self, i):
        try:
            return list(mask)[i]
        except(IndexError):
            return None

    def _set_mouth(self, i):
        try:
            return list(mouth)[i]
        except(IndexError):
            return None

    def _set_bottoms(self, i):
        try:
            return list(bottoms)[i]
        except(IndexError):
            return None

    def _set_boots(self, i):
        try:
            return list(boots)[i]
        except(IndexError):
            return None

    def _set_base_color(self):
        return base_color[_nucleobase(self._dna, 8)]

    def _set_alt_color(self):
        return alt_color[_nucleobase(self._dna, 9)]

    def _set_eye_color(self):
        return eye_color[_nucleobase(self._dna, 10)]

    def _set_skin_color(self):
        return skin_color[_nucleobase(self._dna, 11)]

    def get_colored_parts(self):
        return [self._base_color, self._alt_color, self._eyes, self._skin]

    def __str__(self):
        return(f"Luchador{self._id:<5}"
                f"Colors({self._base_color}/{self._alt_color} "
                f"eyes: {self._eyes} skin: {self._skin}) "
                f"Attrs: {self._attributes}"
        )
    def to_svg(self):
        svgname = "luchador" + str(self._id)
        cape_hood = ""
        if self._attributes.get('cape'):
            cape_shoulders = ("<path class='lucha-alt' d='M20 10V9h-2v1h-1v1h4v-1zM5 9H4v1H3v1h4v-1H6V9z'/>"
                    "<path fill='#000' opacity='.2' d='M6 9H4v1H3v1h4v-1H6zM20 10V9h-2v1h-1v1h4v-1z'/>")
            if cape.get(self._attributes.get('cape')) == "Hooded":
                cape_hood = ("<path class='lucha-alt' "
                  "d='M18 4V3h-1V2h-1V1h-1V0H9v1H8v1H7v1H6v2H5v5h1V6h1V5h2V4h1V3h4v1h1v1h2v1h1v4h1V5h-1z'/>"
                  "<g fill='#000'>"
                  "<path d='M18 4V3h-1V2h-1V1h-1V0H9v1H8v1H7v1H6v2H5v5h1V5h1V4h1V3h1V2h6v1h1v1h1v1h1v5h1V5h-1z'"
                  " opacity='.2'/><path d='M16 4V3h-1V2H9v1H8v1H7v1h2V4h1V3h4v1h1v1h2V4zM6 5h1v1H6zM17 5h1v1h-1z' "
                  "opacity='.5'/></g>")
        else:
            cape_shoulders = ""
        svg = (
                f"<svg id='{svgname}' xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'>"
                "<style>#" + svgname + " .lucha-base { fill: #" + self._base_color + "; } "
                "#" + svgname + " .lucha-alt { fill: #" + self._alt_color + "; } "
                "#" + svgname + " .lucha-eyes { fill: #" + self._eyes + "; } "
                "#" + svgname + " .lucha-skin { fill: #" + self._skin + "; } "
                "#" + svgname + " .lucha-breathe { animation: 0.5s lucha-breathe infinite alternate ease-in-out; }"
                " @keyframes lucha-breathe { from { transform: translateY(0px); } to { transform: translateY(1%); } }"
                "</style>"
                "<g class='lucha-breathe'>"
                + spirit.get(self._attributes.get('spirit'), '')
                + cape.get(self._attributes.get('cape'), '')
                + "<path class='lucha-skin' d='M22 "
                + "12v-1h-1v-1h-1V9h-1V5h-1V3h-1V2h-1V1h-1V0H9v1H8v1H7v1H6v2H5v4H4v1H3v1H2v1H1v8h4v-1h1v-2H5v-3h1v1h1v1h1v2h8v-2h1v-1h1v-1h1v3h-1v2h1v1h4v-8z'/>"
                + torso.get(self._attributes.get('torso'), '')
                + arms.get(self._attributes.get('arms'), '')
                + cape_shoulders + "<path class='lucha-base' "
                + "d='M18 5V3h-1V2h-1V1h-1V0H9v1H8v1H7v1H6v2H5v5h1v2h1v1h1v1h1v1h6v-1h1v-1h1v-1h1v-2h1V5z'/>"
                + "<g class='lucha-alt'>"
                + mask.get(self._attributes.get('mask'), '') + "</g>"
                + cape_hood
                + "<path fill='#FFF' d='M9 6H6v3h4V6zM17 6h-3v3h4V6z'/><path class='lucha-eyes' "
                + "d='M16 6h-2v3h3V6zM8 6H7v3h3V6H9z'/><path fill='#FFF' d='M7 6h1v1H7zM16 6h1v1h-1z' "
                + "opacity='.4'/><path fill='#000' d='M15 7h1v1h-1zM8 7h1v1H8z'/><path class='lucha-skin' "
                + "d='M14 10H9v3h6v-3z'/><path fill='#000' opacity='.9' d='M13 11h-3v1h4v-1z'/>"
                + mouth.get(self._attributes.get('mouth'), '')
                + "</g><path class='lucha-skin' d='M16 23v-6H8v6H7v1h4v-4h2v4h4v-1z'/>"
                + "<path class='lucha-base' d='M15 17H8v1h1v1h2v1h2v-1h2v-1h1v-1z'/>"
                + bottoms.get(self._attributes.get('bottoms'), '')
				+ "<path class='lucha-base' d='M9 21H8v2H7v1h4v-3h-1zM16 23v-2h-3v3h4v-1z'/>"
                + boots.get(self._attributes.get('boots'), '')
                + "</svg>"
        )
        return svg

    # Class methods
    def totalSupply():
        return 10_000

    def attributes_names():
        return ['spirit', 'cape', 'torso', 'arms', 'mask', 'mouth', 'bottoms', 'boots']

    def colored_part_names():
        return ['base', 'alt', 'eyes', 'skin']

# Tools
def _nucleobase(dna, index):
    """ Returns a single-digit from the dna """
    return int(dna[-index - 1])

# Colors and Attributes

# Tools
def _nucleobase(dna, index):
    """ Returns a single-digit from the dna """
    return int(dna[-index - 1])

# Colors and Attributes
base_color = [
        "ebebf7", "1c1d2f", "cc0d3d", "d22f94", "890ec1",
        "1c49d8","19b554", "13cac6", "f7c23c", "f18e2f"
    ]
alt_color = [
        "dadae6", "13141f", "ea184d", "e0369f", "9511d2",
        "2854e6", "1da951", "11b9b5", "e8b63a", "e28327"
    ]
eye_color = [
        "3b6ba5", "3b8fa5", "3ba599", "3ba577", "339842",
        "7fa53b", "a5823b", "a5693b", "844f1d", "4e2906"
    ]
skin_color = ["f9d1b7", "f7b897", "f39c77", "ffcb84", "bd7e47",
        "b97e4b", "b97a50", "5a3214", "50270e", "3a1b09"
        ]

spirit = OrderedDict()
spirit['Bull'] = "<path fill='#A9A18A' d='M21 2V1h-1V0h-1v2h1v1h-3v2h2v1h2V5h1V2zM5 3H4V2h1V0H4v1H3v1H2v3h1v1h2V5h2V3H6z'/><g fill='#000' opacity='.15'><path d='M21 4h1v1h-1zM19 5h-1v1h3V5h-1z'/><path d='M2 4h1v1H2zM4 5H3v1h3V5H5z'/></g>"
spirit['Jaguar'] = "<path class='lucha-base' d='M6 2V1H5v5h1V5h1V3h1V2H7zM18 1v1h-2v1h1v2h1v1h1V1z'/><g fill='#000'><path d='M5 1h1v1H5zM6 2v1h2V2H7zM18 1h1v1h-1zM16 2v1h2V2h-1z' opacity='.3'/><path d='M6 3V2H5v4h1V5h1V3zM18 2v1h-1v2h1v1h1V2z' opacity='.2'/></g>"
cape = OrderedDict()
cape['Classic'] = "<path class='lucha-alt' d='M20 11H3v12h1v-1h2v-1h12v1h2v1h1V11z'/><g fill='#000'><path opacity='.2' d='M20 11v12h1V11zM3 12v11h1V11H3z'/><path opacity='.5' d='M19 11H4v11h2v-1h12v1h2V11z'/></g>"
cape['Hooded'] = "<path class='lucha-alt' d='M20 11H3v12h1v-1h2v-1h12v1h2v1h1V11z'/><g fill='#000'><path opacity='.2' d='M20 11v12h1V11zM3 12v11h1V11H3z'/><path opacity='.5' d='M19 11H4v11h2v-1h12v1h2V11z'/></g>"
torso = OrderedDict()
torso['Shirt'] = "<path class='lucha-base' d='M22 12v-1h-1v-1h-1V9H4v1H3v1H2v1H1v5h4v-3h1v1h1v1h1v2h8v-2h1v-1h1v-1h1v3h4v-5z'/><path d='M22 12v-1h-1v-1h-1V9H4v1H3v1H2v1H1v5h4v-3h1v1h1v1h1v2h8v-2h1v-1h1v-1h1v3h4v-5z' fill='#000' opacity='.15'/>"
torso['Open Shirt'] = "<path class='lucha-base' d='M10 9H4v1H3v1H2v1H1v3h4v-1h1v1h1v1h1v2h3V9zM22 12v-1h-1v-1h-1V9h-7v9h3v-2h1v-1h1v-1h1v1h4v-3z'/><path d='M10 9H4v1H3v1H2v1H1v3h4v-1h1v1h1v1h1v2h3V9zM22 12v-1h-1v-1h-1V9h-7v9h3v-2h1v-1h1v-1h1v1h4v-3z' fill='#000' opacity='.15'/>"
torso['Singlet'] = "<path class='lucha-base' d='M16 9H7v3h1-1v4h1v1h8v-1h1v-4h-1 1V9z'/><path fill='#000' opacity='.15' d='M16 9H7v7h1v1h8v-1h1V9z'/>"
torso['Suspenders'] = "<path class='lucha-base' d='M15 9v9h1V9zM8 10v8h1V9H8z'/><path d='M8 10v8h1V9H8zM15 9v9h1V9z' fill='#000' opacity='.15'/>"
arms = OrderedDict()
arms['Gloves'] = "<path class='lucha-base' d='M5 16H1v3h4v-1h1v-1H5zM22 16h-3v1h-1v1h1v1h4v-3z'/><path class='lucha-alt' d='M3 16H1v1h4v-1H4zM22 16h-3v1h4v-1z'/>"
arms['Wrist Bands'] = "<path class='lucha-base' d='M3 15H1v2h4v-2H4zM22 15h-3v2h4v-2z'/>"
arms['Right Band'] = "<path class='lucha-alt' d='M4 14H1v1h4v-1z'/>"
arms['Left Band'] = "<path class='lucha-base' d='M22 14h-3v1h4v-1z'/>"
arms['Arm Bands'] = "<path class='lucha-base' d='M4 14H1v1h4v-1zM22 14h-3v1h4v-1z'/>"
arms['Sleeves'] = "<path class='lucha-base' d='M22 14h-3v3h4v-3zM3 14H1v3h4v-3H4z'/><path class='lucha-alt' d='M22 14h-3v1h4v-1zM3 14H1v1h4v-1H4z'/>"
mask = OrderedDict()
mask['Split'] = "<path d='M11 0H9v1H8v1H7v1H6v2H5v5h1v2h1v1h1v1h1v1h3V0z'/>"
mask['Cross'] = "<path d='M14 2h-1V0h-2v2H9v2h2v4h2V4h2V2zM12 13h-1v2h2v-2z'/>"
mask['Fierce'] = "<path d='M17 3v1h-2v1h-1v1h-1v3h5V3zM11 8V6h-1V5H9V4H7V3H6v6h5zM11 13v2h2v-2h-1z'/>"
mask['Striped'] = "<path d='M11 2h2V1h1V0h-4v1h1zM6 10v2h1v-1h1v-1H7zM17 10h-1v1h1v1h1v-2z'/><path d='M16 3h1V2h-1V1h-1v1h-1v1h-1v1h-2V3h-1V2H9V1H8v1H7v1h1v1h1v1h1v1h1v9h2V6h1V5h1V4h1z'/>"
mask['Bolt'] = "<path d='M13 3h-3V2h1V1h1V0H9v1H8v1H7v1H6v2h3v1H8v2H7v2h1V9h1V8h1V7h1V6h1V5h1V4h1V3z'/>"
mask['Winged'] = "<path d='M18 5V3h-1V2h-1v1h-1v1h-1v1h-1v1h-2V5h-1V4H9V3H8V2H7v1H6v2H5v5h1v2h1v-1h1v-1h3V9h2v1h3v1h1v1h1v-2h1V5z'/>"
mask['Classic'] = "<path d='M18 5V3h-1V2h-1v2h-1v1h-1v1h-1v3h-2V6h-1V5H9V4H8V2H7v1H6v2H5v4h1v1h2v3h1v1h6v-1h1v-3h2V9h1V5z'/>"
mask['Arrow'] = "<path d='M18 5V3h-1V2h-1V1h-1V0H9v1H8v1H7v1H6v2H5v5h1v2h1v1h1v1h1v1h1v-4h1V5H9V3h1V2h1V1h2v1h1v1h1v2h-2v6h1v4h1v-1h1v-1h1v-1h1v-2h1V5z'/>"
mask['Dash'] = "<path d='M13 3V2h-2v2h2zM13 1V0h-2v1h1zM10 4H9V1H8v1H7v1H6v2H5v5h1v2h1v1h1v1h1v1h1v-2H9v-3h2V5h-1zM18 5V3h-1V2h-1V1h-1v3h-1v1h-1v5h2v3h-1v2h1v-1h1v-1h1v-1h1v-2h1V5z'/>"
mouth = OrderedDict()
mouth['Moustache'] = "<path fill='#421c03' opacity='.9' d='M14 10H9v3h1v-2h4v2h1v-3z'/>"
bottoms = OrderedDict()
bottoms['Tights'] = "<path class='lucha-alt' d='M15 17H8v6h3v-3h2v3h3v-6z'/>"
bottoms['Trunk Tights'] = "<path class='lucha-base' d='M15 17H8v3h8v-3z'/><path class='lucha-alt' d='M15 18v1h-2v4h3v-5zM9 19v-1H8v5h3v-4h-1z'/>"
boots = OrderedDict()
boots['Two Tone'] = "<path class='lucha-alt' d='M9 22H8v1H7v1h4v-2h-1zM16 23v-1h-3v2h4v-1z'/>"
boots['High'] = "<path class='lucha-alt' d='M9 20H8v1h3v-1h-1zM15 20h-2v1h3v-1z'/>"
