# m05 調査の結果(economy)

## s05-2 大卒の失業が減った月の原因

問い: 大卒の失業が 7,099 → 6,866 と減った月は、事務所が増えたのか、税の引き上げか、別の原因か。

### 2050-05-11(見回り1)

- `demand_breakdown()`: jobs 86,464、emptyJobs 3,381、homes 55,601、emptyHomes 5,166、unemployed 6,890。byEducation の unemployed は uneducated 132、elementary 29、highSchool 30、university 6,699(eligibleWorkers 82,492)
- `building_stats()`: OfficeGeneric 4,012棟(放棄2)、レベル 69 / 683 / 3,258、jobs 53,533、地価58。CommercialHigh 1,075棟(放棄104)、jobs 7,924。CommercialLow 165棟、jobs 1,493。IndustrialGeneric 806棟(放棄9)、jobs 10,648。ResidentialHigh 4,057棟、homes 52,158、地価58。ResidentialLow 1,013棟、homes 3,443
- `citizens_summary()`: residents 177,754、employed 82,961、unemployed 5,616(young 2,650、adult 2,966。大卒 5,474、高卒 63、小卒 18、学歴なし 61)、students 42,470、longUnemployed 4,676。年齢 子ども 10,684、10代 22,258、若者 32,045、大人 67,338、高齢 45,429。学歴 大卒 121,606

### 2050-05-21(見回り2)

- `demand_breakdown()`: jobs 86,340、emptyJobs 3,459、homes 55,621、emptyHomes 5,244、unemployed 6,818。byEducation の unemployed は uneducated 137、elementary 47、highSchool 22、university 6,612(eligibleWorkers 82,392)
- `building_stats()`: OfficeGeneric 4,012棟(放棄2)、レベル 67 / 683 / 3,260、jobs 53,553、地価58。CommercialHigh 1,078棟(放棄119)、jobs 7,785。CommercialLow 166棟、jobs 1,497。IndustrialGeneric 806棟(放棄12)、jobs 10,585。ResidentialHigh 4,057棟、homes 52,177。ResidentialLow 1,013棟、homes 3,446
- `citizens_summary()`: residents 177,438、employed 82,766、unemployed 5,528(young 2,591、adult 2,937。大卒 5,416、高卒 40、小卒 29、学歴なし 43)、students 42,492、longUnemployed 4,564。年齢 子ども 10,716、10代 22,211、若者 32,008、大人 67,137、高齢 45,366。学歴 大卒 121,455

### 2050-05-31(月末)

- `demand_breakdown()`: jobs 86,249、emptyJobs 3,351、homes 55,644、emptyHomes 5,277、unemployed 6,715。byEducation の unemployed は uneducated 129、elementary 37、highSchool 24、university 6,525(eligibleWorkers 82,291)
- `building_stats()`: OfficeGeneric 4,012棟(放棄1)、レベル 68 / 683 / 3,260、jobs 53,557、地価58。CommercialHigh 1,080棟(放棄122)、jobs 7,735、地価55。CommercialLow 166棟、jobs 1,497。IndustrialGeneric 806棟(放棄13)、jobs 10,603。ResidentialHigh 4,057棟、homes 52,198、地価58。ResidentialLow 1,013棟、homes 3,446
- `citizens_summary()`: residents 177,196、employed 82,842、unemployed 5,409(young 2,501、adult 2,908。大卒 5,298、高卒 32、小卒 29、学歴なし 50)、students 42,400、longUnemployed 4,406。年齢 子ども 10,668、10代 22,134、若者 32,056、大人 67,022、高齢 45,316。学歴 大卒 121,444。健康 77、幸福度 88
- 参考(調査の道具ではない、m05-1 の確かめ): (1928, 1645) の円に事務所が2棟(10647、41581)建った。`economy_breakdown` の Office の収入は 40,091(05-01)→ 39,405(05-31)
