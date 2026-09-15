# Generation III 이식용 배틀 스프라이트 공통 고정 지침

이 작업의 목적은 각 세대에서 확인 가능한 가장 원본에 가까운 공식 그래픽 자산을 조사하고, 그 자산이 가진 형태·색·배치·팔레트·프레임·성별·폼·애니메이션 등의 정보를 가능한 한 손실 없이 보존하면서 Pokémon Generation III에서 실제 사용할 수 있는 64×64 배틀 스프라이트 자산으로 변환·복원·이식하는 것이다.

이 작업은 단순 이미지 축소 작업이 아니다. 또한 임의의 현대화, 재해석, AI 보정, 자동 팔레트 단순화 작업도 아니다. 먼저 원본 자료와 원본 구조를 조사하고, 해당 세대의 실제 구현 방식과 사용 가능한 원본 소스의 성격을 확정한 뒤, Generation III의 기술적 제약에 맞춰 보존 이식한다.

최종 목표는 “64×64 이미지 하나를 만드는 것”이 아니라 원본 출처부터 Generation III용 최종 binary asset까지 전 과정을 재현 가능하고 검증 가능한 형태로 구축하는 것이다.

## 1. 소스 선정 원칙

ROM 또는 게임 내부 데이터가 존재하고 접근 가능한 경우에는 게임 데이터에서 직접 추출·디코드한 그래픽, 팔레트, 인덱스, 프레임, 애니메이션, archive/member 구조를 가장 높은 우선순위의 소스로 사용한다.

그러나 ROM 또는 게임 내부 데이터의 직접 확보를 작업의 필수 조건으로 삼지 않는다.

ROM이 없거나 직접 추출할 수 없는 경우에도 작업을 중단하지 않는다. 공개된 공식 자산, 검증된 추출물, 보존 프로젝트 자료, 공식 렌더, 공식 모델, 공식 텍스처, 게임 내 캡처, 공식 웹사이트 이미지, 공식 배포 자료 등 현재 확인 가능한 자료 가운데 가장 원본에 가까운 소스를 조사하여 사용한다.

즉 소스 선정의 최상위 원칙은 다음과 같다.

> ROM 보유 여부가 기준이 아니라, 해당 세대에서 확인 가능한 가장 원본에 가깝고 검증 가능한 공식 또는 보존 소스를 우선한다.

동일 자산이 여러 출처에 존재한다면 해상도, 픽셀 구조, 팔레트, 투명색, 프레임, 메타데이터, SHA-256 등을 비교하여 어느 자료가 가장 원본에 가까운지 판단한다.

웹 미리보기, 확대 PNG, 팬사이트 미러, 스크린샷 등이 유일한 자료라면 사용할 수 있다. 그러나 이를 게임 내부 원본과 동일하다고 자동으로 간주하지 않는다. 확대·축소·압축·필터링·안티앨리어싱 과정에서 생성된 중간색을 실제 원본 팔레트 색으로 오인해서는 안 된다.

## 2. 세대·작품별 원본 구조를 먼저 조사한다

모든 세대와 작품이 동일한 그래픽 구조를 사용한다고 가정하지 않는다.

변환 전에 해당 작품에서 실제로 사용하는 native canvas 크기, front/back 구조, frame 수, male/female 차이, normal/shiny, alternate form, palette 구조, transparent index, sprite archive 구조, animation 구조, static sprite와 animated parts의 관계, 실제 로딩 루틴과 slot 관계를 조사한다.

Generation IV와 Generation V처럼 게임 내부에 indexed battle sprite가 실제로 존재하는 경우에는 해당 indexed 구조와 palette index를 최대한 그대로 보존한다.

반대로 후대의 3D 세대처럼 공식적인 2D battle sprite가 존재하지 않는 경우에는 존재하지 않는 2D 원본을 임의로 만들어 “원본”이라고 부르지 않는다.

그 경우에는 공식 모델, 텍스처, 인게임 렌더링, 공식 일러스트, 공식 캡처 등 가운데 가장 적절한 자료를 canonical visual source로 확정하고, 그 source를 기반으로 Generation III용 2D sprite를 제작한다.

## 3. Generation III 목표 규격

최종 Pokémon battle sprite는 Generation III 엔진에서 실제 사용할 수 있는 64×64 canvas 기반 자산으로 변환한다.

단순 PNG만 만드는 것으로 작업을 끝내지 않는다.

최종 자산은 Generation III에서 실제로 사용할 수 있는 indexed/4bpp-compatible 구조까지 완성해야 하며, palette 및 압축 자산도 함께 생성한다.

## 4. 원본이 indexed sprite인 경우

원본 게임에 실제 palette index 기반 battle sprite가 존재하는 경우에는 RGB 이미지로 변환한 뒤 다시 색을 추측하여 새 palette를 만드는 방식을 사용하지 않는다.

가능한 한 처음부터 원본 palette index 상태를 유지한다.

Generation IV BATTLE_MASTER_V1의 preservation-v2 방식처럼 원본 전체 source canvas를 Generation III 전체 64×64 target canvas에 직접 대응시킨다.

포켓몬 본체의 opaque bounding box만 잘라서 64×64에 꽉 채우거나, 종마다 크기를 인위적으로 정규화하지 않는다.

원본 게임에서의 상대적 크기, 화면 내 위치, 상하좌우 여백, 전투 화면 배치감을 최대한 유지한다.

## 5. preservation-v2 변환 원칙

indexed source를 축소할 때 일반 이미지 resize 알고리즘으로 처리하지 않는다.

각 64×64 target pixel에 대응되는 source 영역을 계산하고, 그 영역과 실제 source pixel 사이의 정확한 면적 overlap을 계산한다.

출력 pixel은 겹치는 기존 source palette index 중 하나를 선택한다.

RGB 평균값을 계산하여 새 색을 만들지 않는다.

희소하지만 눈, 문양, 윤곽, 강조색, 작은 장식 등 포켓몬 식별에 중요한 index가 과도하게 사라지지 않도록 mild rare-color preservation을 적용한다.

투명 영역 때문에 실루엣이 과도하게 깎이는 현상도 방지한다. target pixel에 대응되는 source footprint의 절반 이상이 opaque인 경우 transparency가 해당 pixel을 이기지 못하게 하는 silhouette protection 규칙을 적용한다.

## 6. 색상 처리 고정 규칙

생성형 이미지 도구를 사용하지 않는다.

AI redraw, AI retouch, AI upscaling, 안티앨리어싱, RGB interpolation, bilinear, bicubic, 평균색 생성, 중간색 생성, 원본에 존재하지 않는 새로운 색 생성은 금지한다.

원본이 indexed sprite라면 원본 palette와 palette index를 최대한 유지한다.

“Generation III는 16색이므로 사용 빈도가 높은 색 15개를 자동으로 뽑는다”는 방식은 사용하지 않는다.

색상의 사용 빈도와 시각적 중요성은 동일하지 않다.

눈, 줄무늬, 문양, 금속 장식, 포켓몬 특유의 강조색, 희소한 하이라이트 등은 pixel 수가 적더라도 종의 시각적 정체성을 결정할 수 있다.

기술적으로 16색 제한을 충족한다는 이유만으로 해당 포켓몬의 대표색을 제거해서는 안 된다.

## 7. 원본이 true-color 또는 3D인 경우

후대 세대처럼 Generation III식 indexed 2D sprite가 존재하지 않는 경우에는 indexed-source 규칙을 기계적으로 적용하지 않는다.

먼저 해당 포켓몬의 공식 디자인에서 어떤 요소가 시각적 정체성을 구성하는지 조사한다.

몸체의 기본색, 어두운 영역, 윤곽, 하이라이트, 눈, 문양, 장식, 금속부, 발광부, 날개, 꼬리 등 핵심 구성요소를 분석한 뒤 Generation III의 제한된 palette 안에서 최대한 보존한다.

이 경우에도 단순 자동 빈도순 색 축소를 사용하지 않는다.

최종 결과를 보았을 때 원본 포켓몬과 즉시 같은 종으로 인식될 수 있도록 형태와 상징색 보존을 우선한다.

## 8. 확대 PNG 또는 웹 이미지밖에 없는 경우

확대 PNG나 웹 이미지도 source로 사용할 수 있다.

그러나 이를 실제 indexed source와 동일하게 취급하지 않는다.

확대 또는 필터링 과정에서 원본에는 없던 수백~수천 개의 RGB 중간색이 생길 수 있기 때문이다.

따라서 확대 RGB PNG에서 단순히 “대표 16색”을 다시 추출하여 final asset으로 확정하는 방식을 금지한다.

먼저 원본 해상도 자료, 다른 공식 자료, 보존 프로젝트, 공개 추출 자산 등을 추가 조사한다.

더 나은 source를 확보하지 못한 경우에는 해당 자산이 reconstructed/provisional source임을 명시하고, 사용한 자료와 변환 한계를 manifest에 기록한다.

## 9. 시각 검수는 필수다

자동 변환이 정상 종료되었다는 이유만으로 결과를 승인하지 않는다.

원본과 최종 결과를 반드시 나란히 비교한다.

실루엣, 머리, 얼굴, 눈, 날개, 꼬리, 팔다리, 문양, 대표색, 밝기 대비, 하이라이트, 장식, 전체적인 인상을 확인한다.

특히 포켓몬의 대표적인 색이나 특징이 손실되어 다른 캐릭터처럼 보인다면 기술적으로 64×64이고 palette 제한을 통과했더라도 실패로 처리한다.

최종 결과는 반드시 원본 포켓몬처럼 보여야 한다.

Generation III 제약을 만족하는 것과 포켓몬의 정체성을 보존하는 것은 동시에 충족되어야 한다.

## 10. 자동 처리와 수동 픽셀 보정

가능한 작업은 deterministic script로 재현 가능하게 수행한다.

그러나 자동 변환으로 눈, 문양, 실루엣, 작은 장식 등이 명백하게 훼손되는 경우에는 최소한의 수동 pixel correction을 허용한다.

수동 보정은 새로운 디자인을 만드는 작업이 아니다.

Generation III의 제약 때문에 손실된 원본 정보를 복원하는 목적으로만 수행한다.

수동 수정이 발생하면 자동 결과와 수정 결과를 분리하고, 수정 위치와 이유를 manifest 또는 validation 기록에 남긴다.

## 11. 모든 최종 산출물은 의무다

다음 산출물은 선택 사항이 아니다. 모든 배틀 스프라이트 작업에서 반드시 전부 생성하고 전부 보존한다.

- 실제 확인 가능한 최종 PNG
- 원본 source PNG 또는 원본 복원 이미지
- 원본 palette 데이터
- Generation III용 palette 데이터
- Generation III 4bpp 그래픽 데이터
- Generation III용 압축 그래픽 데이터
- source-to-target manifest
- source provenance 기록
- source archive/member 또는 원본 자산 위치 정보
- source SHA-256
- intermediate SHA-256
- final PNG SHA-256
- final rendered-pixel SHA-256
- final palette SHA-256
- final 4bpp SHA-256
- final compressed binary SHA-256
- source → target 대응표
- logical slot → canonical asset 대응표
- 중복 asset 및 SHA-256 dedup 관계
- 변환에 사용한 script와 설정값
- 자동 변환 결과
- 수동 보정 결과 및 수정 이력
- 원본과 최종 결과 비교 자료
- validation 결과 및 오류 기록
- 재빌드 및 재현에 필요한 모든 메타데이터

PNG만 존재하는 상태는 완료가 아니다.

palette만 존재하는 상태도 완료가 아니다.

4bpp, 압축 데이터, manifest, SHA-256, validation 중 하나라도 빠져 있으면 완료로 인정하지 않는다.

최종 목표는 단순 시각 자료가 아니라 Generation III 엔진에 실제 삽입 가능하고, 출처와 변환 과정을 완전히 추적할 수 있으며, 동일한 결과를 다시 재생성할 수 있는 전체 자산 패키지다.

## 12. 중복 자산 처리

서로 다른 작품, 버전, 언어, 지역, 리비전, 성별, 폼, 프레임, palette slot에서 생성된 결과라도 최종 rendered pixel 결과가 완전히 동일하면 파일을 중복 저장하지 않는다.

최종 rendered result의 SHA-256을 기준으로 동일 자산을 전역 deduplicate하고 하나의 canonical asset만 보관한다.

단, 어떤 게임·버전·폼·프레임·논리적 slot이 해당 canonical asset을 참조하는지는 manifest에 전부 기록한다.

중복 파일을 제거하더라도 논리적 관계는 절대 삭제하지 않는다.

## 13. provenance와 검증 기록

모든 자산은 어디서 왔고 어떻게 변환되었는지 추적 가능해야 한다.

세대, 작품, 버전, 지역, 언어, 리비전, source 종류, archive/member, native canvas 크기, palette 구조, transparent index, frame, gender, shiny 상태, form, 변환 방식, 수동 수정 여부, source SHA-256, final SHA-256 등을 기록한다.

확인되지 않은 정보는 사실처럼 적지 않는다.

미확인 또는 추정 상태를 명시하고 후속 검증 대상으로 남긴다.

## 14. Sakurai / Tsubaki 저장소 역할

Sakurai에는 조사 자료, source mapping, ROM/archive/member 분석, conversion script, manifest, validation, SHA-256 목록, dedup table, provenance, 비교 자료, 검증 결과를 저장한다.

Tsubaki에는 실제 Generation III에서 사용할 최종 PNG, palette, 4bpp, 압축 데이터, canonical sprite asset 및 모든 삽입용 그래픽 자산을 저장한다.

ROM, cartridge image, ISO 등 원본 게임 바이너리 자체만 GitHub 업로드 대상에서 제외한다.

그 외 프로젝트에서 생성·복원·추출·변환·검증한 모든 작업물은 GitHub에 보존한다.

# 최상위 고정 원칙

- ROM이 없다는 이유로 작업을 중단하지 않는다.
- 해당 세대에서 확인 가능한 가장 원본에 가까운 공식 또는 검증 가능한 보존 자료를 찾아 사용한다.
- 원본이 indexed sprite라면 기존 palette/index 구조를 최대한 그대로 보존한다.
- 원본이 true-color 또는 3D source라면 해당 포켓몬의 시각적 정체성과 대표색을 우선하여 Generation III용 자산으로 재구성한다.
- 확대 RGB PNG에서 자동 빈도순으로 색을 줄여 16색 final asset을 만드는 방식은 금지한다.
- 생성형 이미지 도구는 사용하지 않는다.
- 64×64·4bpp·palette 제한을 만족하는 것만으로 완료되지 않는다. 원본 포켓몬의 형태와 시각적 정체성이 반드시 보존되어야 한다.
- PNG, palette, 4bpp, 압축 데이터, manifest, SHA-256, source mapping, dedup 자료, validation 자료를 포함한 모든 산출물은 반드시 전부 생성하고 전부 보존한다. 선택 사항은 없다.
