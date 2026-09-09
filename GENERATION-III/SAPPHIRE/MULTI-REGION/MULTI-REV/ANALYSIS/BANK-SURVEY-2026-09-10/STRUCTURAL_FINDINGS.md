# Sapphire 64 KiB bank survey — structural findings

- ROMs: 9
- Logical bank: 64 KiB (`0x10000`)
- Total bank-images: 2,176

## AXPJ_rev0

- Validated aligned LZ77 streams: **3184**
- `FF_blank`: `66`
- `compression_candidate_dense`: `1E-24 26-29 2F-33 42 4C-4D 51 54 56 5B-5C 67-7F`
- `high_entropy`: `43-4B 4E-50 52-53 55 57-5A 5D-5F`
- `pointer_dense`: `00-1D 25 2A-2E 34-41 60-65`
- Highest inbound-pointer banks: 0x34=2308, 0x3A=1991, 0x00=1963, 0x3E=1789, 0x3B=1630, 0x1A=1529, 0x3D=1522, 0x1B=1483
- Highest outbound-pointer banks: 0x34=4671, 0x3A=2639, 0x36=2213, 0x35=2120, 0x1C=2003, 0x39=1981, 0x3D=1936, 0x2D=1910
- LZ77-heavy banks: 0x69=231, 0x68=219, 0x6A=184, 0x7F=172, 0x7D=153, 0x7E=131, 0x72=101, 0x77=100

## AXPD_rev1

- Validated aligned LZ77 streams: **3154**
- `FF_blank`: `6C-CF EC-FF`
- `compression_candidate_dense`: `1B 22-28 2A-2C 2E 30 32-36 42 47 4C 51-52 56 59 5B 5F-60 D0-EA`
- `high_entropy`: `48-4B 4D-50 53-55 57-58 5A 5C-5E 61-64`
- `mixed`: `17-19 1C`
- `pointer_dense`: `00-16 1A 1D-21 29 2D 2F 31 37-41 43-46 65-6B`
- `sparse`: `EB`
- Highest inbound-pointer banks: 0x1E=2496, 0x15=2281, 0x3E=2105, 0x37=1822, 0x41=1811, 0x00=1789, 0x1F=1465, 0x40=1460
- Highest outbound-pointer banks: 0x37=3510, 0x38=3053, 0x1F=2730, 0x31=2505, 0x39=2465, 0x3D=2280, 0x3E=2195, 0x3C=2034
- LZ77-heavy banks: 0xD0=245, 0xD2=214, 0xD1=207, 0xE7=152, 0xE5=150, 0xE6=129, 0xDA=104, 0xDE=98

## AXPE_rev1

- Validated aligned LZ77 streams: **3147**
- `FF_blank`: `6C-CF EB-FF`
- `compression_candidate_dense`: `1A-1B 21-27 29-2C 2F 32-35 41-42 46 50-51 55 58 5A 5F-60 D0-EA`
- `high_entropy`: `47-4F 52-54 56-57 59 5B-5E 61-63`
- `mixed`: `17-19 31 3A`
- `pointer_dense`: `00-16 1C-20 28 2D-2E 30 36-39 3B-40 43-45 64-6A`
- `sparse`: `6B`
- Highest inbound-pointer banks: 0x37=2617, 0x1E=2482, 0x3D=2360, 0x15=2310, 0x40=1899, 0x00=1788, 0x1D=1543, 0x0C=1421
- Highest outbound-pointer banks: 0x37=4403, 0x38=2758, 0x1E=2558, 0x30=2553, 0x3D=2524, 0x3C=2307, 0x3B=1975, 0x14=1736
- LZ77-heavy banks: 0xD0=245, 0xD2=212, 0xD1=209, 0xE7=153, 0xE5=150, 0xE6=129, 0xDA=103, 0xDE=98

## AXPE_rev0

- Validated aligned LZ77 streams: **3150**
- `FF_blank`: `6C-CF EB-FF`
- `compression_candidate_dense`: `1B 21-27 29-2C 2F 32-35 41-42 46 50-51 55 58 5A 5F-60 D0-EA`
- `high_entropy`: `47-4F 52-54 56-57 59 5B-5E 61-63`
- `mixed`: `17-19 31 3A`
- `pointer_dense`: `00-16 1A 1C-20 28 2D-2E 30 36-39 3B-40 43-45 64-6A`
- `sparse`: `6B`
- Highest inbound-pointer banks: 0x37=2617, 0x1E=2483, 0x3D=2361, 0x15=2308, 0x40=1901, 0x00=1789, 0x1D=1544, 0x0C=1420
- Highest outbound-pointer banks: 0x37=4401, 0x38=2757, 0x1E=2557, 0x30=2553, 0x3D=2524, 0x3C=2307, 0x3B=1975, 0x14=1737
- LZ77-heavy banks: 0xD0=245, 0xD2=212, 0xD1=209, 0xE7=153, 0xE5=150, 0xE6=129, 0xDA=103, 0xDE=98

## AXPE_rev2

- Validated aligned LZ77 streams: **3147**
- `FF_blank`: `6C-CF EB-FF`
- `compression_candidate_dense`: `1A-1B 21-27 29-2C 2F 32-35 41-42 46 50-51 55 58 5A 5F-60 D0-EA`
- `high_entropy`: `47-4F 52-54 56-57 59 5B-5E 61-63`
- `mixed`: `17-19 31 3A`
- `pointer_dense`: `00-16 1C-20 28 2D-2E 30 36-39 3B-40 43-45 64-6A`
- `sparse`: `6B`
- Highest inbound-pointer banks: 0x37=2617, 0x1E=2482, 0x3D=2360, 0x15=2310, 0x40=1899, 0x00=1788, 0x1D=1543, 0x0C=1421
- Highest outbound-pointer banks: 0x37=4403, 0x38=2758, 0x1E=2558, 0x30=2553, 0x3D=2524, 0x3C=2307, 0x3B=1975, 0x14=1736
- LZ77-heavy banks: 0xD0=245, 0xD2=212, 0xD1=209, 0xE7=153, 0xE5=150, 0xE6=129, 0xDA=103, 0xDE=98

## AXPF_rev1

- Validated aligned LZ77 streams: **3150**
- `FF_blank`: `6C-CF EC-FF`
- `compression_candidate_dense`: `1B 22-27 29-2C 2F 31-36 46-47 50-52 58-5A 5F-60 63 D0-EA`
- `high_entropy`: `48-4F 53-57 5B-5E 61-62`
- `mixed`: `17-19`
- `pointer_dense`: `00-16 1A 1C-21 28 2D-2E 30 37-41 43-45 64-6B`
- `sparse`: `42 EB`
- Highest inbound-pointer banks: 0x1E=2582, 0x37=2352, 0x15=2270, 0x3E=1933, 0x41=1874, 0x3D=1800, 0x00=1788, 0x0C=1417
- Highest outbound-pointer banks: 0x37=4801, 0x1F=2817, 0x38=2640, 0x30=2502, 0x3D=2313, 0x3E=1964, 0x3C=1898, 0x45=1730
- LZ77-heavy banks: 0xD0=245, 0xD2=214, 0xD1=207, 0xE7=153, 0xE5=150, 0xE6=129, 0xDA=104, 0xDE=98

## AXPF_rev0

- Validated aligned LZ77 streams: **3150**
- `FF_blank`: `6C-CF EC-FF`
- `compression_candidate_dense`: `1B 22-27 29-2C 2F 31-36 46-47 50-52 58-5A 5F-60 63 D0-EA`
- `high_entropy`: `48-4F 53-57 5B-5E 61-62`
- `mixed`: `17-19`
- `pointer_dense`: `00-16 1A 1C-21 28 2D-2E 30 37-41 43-45 64-6B`
- `sparse`: `42 EB`
- Highest inbound-pointer banks: 0x1E=2582, 0x37=2352, 0x15=2270, 0x3E=1933, 0x41=1874, 0x3D=1800, 0x00=1788, 0x0C=1417
- Highest outbound-pointer banks: 0x37=4801, 0x1F=2817, 0x38=2640, 0x30=2502, 0x3D=2313, 0x3E=1964, 0x3C=1898, 0x45=1730
- LZ77-heavy banks: 0xD0=245, 0xD2=214, 0xD1=207, 0xE7=153, 0xE5=150, 0xE6=129, 0xDA=104, 0xDE=98

## AXPI_rev1

- Validated aligned LZ77 streams: **3157**
- `FF_blank`: `6C-CF EC-FF`
- `compression_candidate_dense`: `1B 21-27 29-2C 2F 32-35 3A 41 46-47 49 50-51 55 58 5A 5F-60 D0-EA`
- `high_entropy`: `48 4A-4F 52-54 56-57 59 5B-5E 61-63`
- `mixed`: `17-19 31 42 6B`
- `pointer_dense`: `00-16 1A 1C-20 28 2D-2E 30 36-39 3B-40 43-45 64-6A`
- `sparse`: `EB`
- Highest inbound-pointer banks: 0x37=2624, 0x15=2271, 0x1E=2204, 0x3D=2018, 0x40=1905, 0x00=1789, 0x3E=1689, 0x1D=1534
- Highest outbound-pointer banks: 0x37=4492, 0x38=2815, 0x1E=2591, 0x3D=2487, 0x30=2472, 0x3C=2299, 0x3B=1975, 0x14=1729
- LZ77-heavy banks: 0xD0=245, 0xD2=214, 0xD1=207, 0xE7=152, 0xE5=149, 0xE6=130, 0xDA=104, 0xDE=98

## AXPI_rev0

- Validated aligned LZ77 streams: **3157**
- `FF_blank`: `6C-CF EC-FF`
- `compression_candidate_dense`: `1B 21-27 29-2C 2F 32-35 3A 41 46-47 49 50-51 55 58 5A 5F-60 D0-EA`
- `high_entropy`: `48 4A-4F 52-54 56-57 59 5B-5E 61-63`
- `mixed`: `17-19 31 42 6B`
- `pointer_dense`: `00-16 1A 1C-20 28 2D-2E 30 36-39 3B-40 43-45 64-6A`
- `sparse`: `EB`
- Highest inbound-pointer banks: 0x37=2624, 0x15=2271, 0x1E=2204, 0x3D=2018, 0x40=1905, 0x00=1789, 0x3E=1689, 0x1D=1534
- Highest outbound-pointer banks: 0x37=4492, 0x38=2815, 0x1E=2591, 0x3D=2487, 0x30=2472, 0x3C=2299, 0x3B=1975, 0x14=1729
- LZ77-heavy banks: 0xD0=245, 0xD2=214, 0xD1=207, 0xE7=152, 0xE5=149, 0xE6=130, 0xDA=104, 0xDE=98

## Exact minor-revision byte changes

- **AXPE_rev1 → AXPE_rev2**: 0x000000BC 01→02, 0x000000BD 54→53, 0x0000919B DD→DB, 0x000091BF DC→DA
- **AXPF_rev0 → AXPF_rev1**: 0x000000BC 00→01, 0x000000BD 54→53, 0x00009367 DD→DB, 0x0000938B DC→DA
- **AXPI_rev0 → AXPI_rev1**: 0x000000BC 00→01, 0x000000BD 51→50, 0x00009367 DD→DB, 0x0000938B DC→DA

## Interpretation

- Banks classified `FF_blank` are all- or nearly-all-FF allocation gaps and should not be treated as semantic content.
- Pointer-graph in/out counts are a stronger structural signal than raw byte entropy alone.
- `validated_lz77_aligned4` parses the stream, so it is substantially more reliable than a raw `0x10` header count.
- Semantic labels still require symbol/source anchoring; English Rev0 can be anchored directly to pret/pokeruby because the SHA-1 matches exactly.
