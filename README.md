# mask_blockchain  

台湾に習い、マスクを一週間に2枚配るためのブロックチェーン。  
mask_blockchainです  
webページは一切デザインしていません  
トランザクションにマイナンバーを12桁で入れるようになっていますが。  
セキュリティの問題上の理由からsha256で2回変換するのが妥当かと思います。  
コメントアウトされている関数の中にsha256で2回変換してくれる関数があるのでそちらをお使いください。  
「マイナンバーの検索機能。マスクの残り数を地図に表示。」は実装されていません。  
しかし、実装しやすいようになっています。