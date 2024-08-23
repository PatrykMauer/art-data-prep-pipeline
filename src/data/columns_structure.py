columns_to_remove = [2, 6, 10, 12, 15, 17, 18, 19]

columns_to_select = [
    'ARTIST', 'TECHNIQUE', 'SIGNATURE', 'CONDITION', 'TOTAL DIMENSIONS',
    'YEAR', 'AUCTION DATE', 'URL', 'ImageName'] + ['PRICE']

techniques = [('Oil on board', 'Oil on board'),
              ('Oil on canvas', 'Oil on canvas'),
              ('Oil on panel', 'Oil on panel'),
              ('Oil on paper', 'Oil on paper'),
              ('Gouache', 'Gouache'),
              ('Pastel', 'Pastel'),
              ('Watercolour', 'Watercolour'),
              ('Acrylic on board', 'Acrylic on board'),
              ('Acrylic on canvas', 'Acrylic on canvas'),
              ('Acrylic on panel', 'Acrylic on panel'),
              ('Acrylic on paper', 'Acrylic on paper'),
              ('Giclée', 'Giclée'),
              ('Etching', 'Etching'),
              ('Drypoint', 'Etching'),
              ('Aquatint', 'Etching'),
              ('Lithograph', 'Lithograph'),
              ('Silkscreen / Serigraph', 'Silkscreen / Serigraph'),
              ('Woodcut print', 'Woodcut print'),
              ('Albumen paper process', 'Albumen paper process'),
              ('Ambrotype', 'Ambrotype'),
              ('Autochrome process', 'Autochrome process'),
              ('Blueprint process', 'Blueprint process'),
              ('Bromoil (process)', 'Bromoil (process)'),
              ('C-Print', 'C-Print'),
              ('Cabinet card', 'Cabinet card'),
              ('Calotype', 'Calotype'),
              ('Carbon print', 'Carbon print'),
              ('Carte de visite', 'Carte de visite'),
              ('Collodion', 'Collodion'),
              ('Collodion printing-out paper, P.O.P',
               'Collodion printing-out paper, P.O.P'),
              ('Collotype', 'Collotype'),
              ('Daguerreotype', 'Daguerreotype'),
              ('Digital print', 'Digital print'),
              ('Dye transfer print', 'Dye transfer print'),
              ('Engraving', 'Engraving'),
              ('Ferrotype', 'Ferrotype'),
              ('Gelatin printing-out paper, P.O.P.',
               'Gelatin printing-out paper, P.O.P.'),
              ('Gelatin-silver print', 'Gelatin-silver print'),
              ('Gelatin-silver print (PE)', 'Gelatin-silver print (PE)'),
              ('Gelatin-silver print developing out paper (D.O.P.)',
               'Gelatin-silver print developing out paper (D.O.P.)'),
              ('Gum-bichromate print', 'Gum-bichromate print'),
              ('Intaglio process', 'Intaglio process'),
              ('Mixed media', 'Mixed media'),
              ('Monoprint', 'Monoprint'),
              ('Offset print', 'Offset print'),
              ('Offset', 'Offset print'),
              ('Photogenic drawing', 'Photogenic drawing'),
              ('Photogravure', 'Photogravure'),
              ('Photolithography', 'Photolithography'),
              ('Helio', 'Photolithography'),
              ('Chromography', 'Photolithography'),
              ('Planographic method', 'Planographic method'),
              ('Platinotype', 'Platinotype'),
              ('Polaroid', 'Polaroid'),
              ('Relief process', 'Relief process'),
              ('Salted paper print', 'Salted paper print'),
              ('Single transfer carbroprint', 'Single transfer carbroprint'),
              ('Unknown', 'Unknown'),
              ('Wire photo', 'Wire photo'),
              ('Woodburytype', 'Woodburytype'),
              ('Silk', 'Silkscreen / Serigraph'),
              ('Serigraph', 'Silkscreen / Serigraph'),
              ('Screen', 'Silkscreen / Serigraph'),
              ('Woodcut', 'Woodcut print'),
              ('Gicl', 'Giclée'),
              ('resin', 'Resin'),
              ('Pochoir', 'Pochoir'),
              ('Lino', 'Linocut')
              ]

techniques_to_keep = [
    'Lithograph', 'Silkscreen / Serigraph', 'Etching', 'Offset print',
    'Photogravure', 'Woodcut print', 'Photolithography', 'Mixed media',
    'Pochoir', 'Collotype', 'Linocut']

techniques_map = {
    'Photolithography': 0, 'Photogravure': 0, 'Offset print': 0
}

techniques_order = [
    'Photolithography', 'Photogravure', 'Offset print', 'Pochoir', 'Collotype',
    'Woodcut print', 'Linocut', 'Silkscreen / Serigraph', 'Lithograph',
    'Etching', 'Mixed media']

signatures = [('Hand signed', 'Hand signed'),
              ('Not signed', 'Not signed'),
              ('Plate signed', 'Plate signed'),
              ]

signature_order = ['Not signed', 'Plate signed', 'Hand signed']

conditions = [
    ('Excellent condition', 'Excellent condition'),
    ('New', 'Excellent condition'),
    ('Excellent condition', 'Excellent condition'),
    ('Fair condition', 'Fair condition'),
    ('Age', 'Fair condition'),
    ('Needs restoration', 'Fair condition'),
    ('Good', 'Good condition'),
    ('', 'Good condition'),
    ('Print', 'Good condition'),
]

condition_order = ['Fair condition', 'Good condition', 'Excellent condition']

periods_to_year = [
    ("2010-present", 2018),  # Assuming 'present' as 2023, middle is 2018
    ("1970-1979", 1974),
    ("1980-1989", 1984),
    ("1990-1999", 1994),
    ("1960-1969", 1964),
    ("2000-2009", 2004),
    ("1970-1980", 1975),
    ("1950-1959", 1954),
    ("1960-1970", 1965),
    ("1980-1990", 1985),
    # Assuming 'before' is not significantly before 1700
    ("1700 and before", 1700),
    ("2000-2010", 2005),
    ("1990-2000", 1995),
    ("2020+", 2021),  # Assuming '+' is not significantly after 2020
    ("1920-1929", 1924),
    ("1800-1899", 1850),  # Middle of a century
    ("1950-1960", 1955),
    ("2010-2020", 2015),
    ("1910-1919", 1914),
    ("1930-1939", 1934),
    ("1700-1799", 1750),  # Middle of a century
    ("1940-1949", 1944),
    ("1920-1930", 1925),
    ("1900-1909", 1904),
    ("1910-1920", 1915),
    ("1940-1950", 1945),
    ("1930-1940", 1935),
    ("1750-1800", 1775),
    ("1850-1900", 1875),  # Middle of a half-century
    ("1600-1650", 1625),
    ("1700-1750", 1725),
    ("1800-1850", 1825),  # Middle of a half-century
    ("1900-1910", 1905),
    ("1550-1600", 1575),
    ("1650-1700", 1675),
    ("Pre-1800", 1750),  # Assuming 'pre-1800' as the first half of the 18th century
    ("1450-1500", 1475),
    ("XXI", 2020),
    ("XX", 1950),
    ("XIX", 1850),
    ("XVIII", 1750),
    ("XVII", 1650),
    ("XVI", 1550),
    ("21st", 2020),
    ("20th", 1950),
    ("19th", 1850),
    ("18th", 1750),
    ("17th", 1650),
    ("16th", 1550),
]
