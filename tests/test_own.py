import pytest, datetime

from ionex_formatter.formatter import (
    IonexFile,
    UnknownFormatingError,
    UnknownFormatSpecifier,
    HeaderDuplicatedLine,
    NumericTokenTooBig,
)
from ionex_formatter.ionex_format import (
    IonexHeader_V_1_1,
)
from ionex_formatter.ionex_map import (
    IonexMap,
    GridCell,
)
from ionex_formatter.spatial import (
    SpatialRange,
    DecimalDigitReduceAccuracyError,
)


class TestFormatter():
    def test_1(self):
        formatter = IonexFile()
        with pytest.raises(UnknownFormatingError):
            formatter._verify_formatted(10.0, "I", "1", 2, 0)

    def test_2(self):
        formatter = IonexFile()
        formatter.add_comment("123")

    def test_3(self):
        formatter = IonexFile()
        with pytest.raises(UnknownFormatSpecifier):
            formatter._verify_formatted([1, 2, 3, 5], 'lolo', 'lol', 4, 3)

    def test_4(self):
        formatter = IonexFile()
        with pytest.raises(HeaderDuplicatedLine):
            formatter.set_spatial_grid(
                lat_range=SpatialRange(87.5, -87.5, -2.5),
                lon_range=SpatialRange(-180.0, 180.0, 5.0),
                height_range=SpatialRange(450.0, 450.0, 0.0)
            )
            formatter.set_spatial_grid(
                lat_range=SpatialRange(87.5, -87.5, -2.5),
                lon_range=SpatialRange(-180.0, 180.0, 5.0),
                height_range=SpatialRange(450.0, 450.0, 0.0)
            )

    def test_5(self):
        formatter = IonexFile()
        with pytest.raises(NumericTokenTooBig):
            formatter._get_header_numeric_token(2.5, 1, 5)


class TestIonexFormat:
    def test_1(self):
        header = IonexHeader_V_1_1()
        header._update()

    # def test_2(self):
    #     with pytest.raises(ValueError):
    #         header = IonexHeader_V_1_1()
    #         header.HEADER_FORMATS['test_2'] = "1"
    #         header.make_automatic_label_format_list()
    #         del header.HEADER_FORMATS['test_2']

    def test_3(self):
        with pytest.raises(FileNotFoundError):
            header = IonexHeader_V_1_1()
            header.load_descriptions('/lol/lol')

    def test_4(self):
        header = IonexHeader_V_1_1()
        with pytest.raises(TypeError):
            header.load_descriptions("ionex_formatter/another_header_line_descriptions.json")

    def test_5(self):
        header = IonexHeader_V_1_1()
        header.line_tokens("HGT1 / HGT2 / DHGT")


class TestIonexMap:
    def test_1(self, map_data):
        cells = GridCell.get_list_from_csv(map_data)
        ionex_map = IonexMap(lat_range=SpatialRange(87.5, -87.5, -87.5),
                             lon_range=SpatialRange(180, -180, -5),
                             height=450,
                             epoch=datetime.datetime(2010, 12, 28)
                             )
        ionex_map.set_data(cells)


class TestSpatial:
    def test_1(self):
        spatial = SpatialRange(100, 0, -5)
        spatial.verify()

    def test_2(self):
        with pytest.raises(DecimalDigitReduceAccuracyError):
            SpatialRange(100.05, 50, -5, 1)

    def test_3(self):
        with pytest.raises(DecimalDigitReduceAccuracyError):
            SpatialRange(100, 50.05, -5, 1)
