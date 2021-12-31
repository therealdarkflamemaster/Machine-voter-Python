# Machine-voter-lectronique_Python
Le but de ce projet informatique est de vous faire créer une simulation de machine à voter securisé. La principale limitation du projet réside dans le fait que, dans un contexte opérationel, plusieurs entité distante et distincte doivent être impliquée ; dans notre projet les entités seront toutes hébergés sur le même ordinateur hôte.

# 项目基本信息

实际程序中，用`一个machine`和`一个人`来做演示就可以了

- 人物
    - `A` : représente **l’autorité** d’administration de l’élection. 选举机构
    - `E` : est l’autorité d’**enregistrement des utilisateurs (le serveur qui créer les accés)**. 登记用户的机构
    - `S` : est **le serveur de vote**, celui sur lesque les électeur mettent leur bulletin. 投票服务器
    - `T1,...,TI` : sont les i utilisateurs de confiance chargées du dépouillement. 负责点票的用户
    - `V1, ..., Vn, ..., VN` : sont les voteurs. 投票者

- 流程
    - **Mise en place d’une élection**
        1. 服务器`A`初始选举流程，`T1,...,TI`  给其投票者`V1, ..., Vn, ..., VN` 的信息（nom,prenom, adresse mail）
        2. `A`给每个用户一个`uuid`，然后把这些信息发给`E`
        3. `E`生成，每个用户的`cn`和`Pub(cn)`
            - `cn` 是 identifiant secret
            - `Pub(cn)` 是 code de vote
        4. `E`给每个用户`V1, ..., Vn, ..., VN`发送他的`cn`
        5. `E`给`A`发送一个list `L`，`E`有能力去删除`cn`的liste
            - `L`= shuffle (Pub(c1)，.... , Pub(cN))
        6. `A`向负责点票的用户`T1,...,TI` 要其的公钥`ai`
        7. 选举信息`D`进入服务器`A`
            - `D` 包括、
                - 选举本身的信息，被选举人的名字，开始和结束时间，怎么投票（用户`V1, ..., Vn, ..., VN` 投票的时候也能看到这些信息）
                - 公钥`ai`
                - liste `L`
                - 所有的bulletins : `B` = (b1, ... , bJ ).
                - 如果选举已经结束，选举结果的信息也会显示
        8. `A`给`S`提供`L`和`D`
    - **Phase de vote**
      
        投票者可以验证自己的选票是否被计入（有一张大表上面写了谁投了谁，用hash标记identifiant）
        
        1. 投票者如果要进行投票，先连接上服务器，得到关于本次选举的知识。
        2. 选举者做出自己的选择，用做公钥的数字，然后用`Pub(cn)`在自己的bulletin上登记
        3. bulletin上还有 一个 signature（用作 Zero -knowledge proof），用作证明这个bulletin已经被知道`cn`的人填好了并且签名了
        4. 服务器验证投票的有效性然后登记在案
            - code在自己的liste上存在
            - 确认知道`cn`的事实
        5. 在选举进行的时候，投票者可以用signature来查看自己的选票
        6. 投票者可以验证自己的选票是否被计入（有一张大表上面写了所有的signature）
    - **Phase d’audit**
      
        `T1; : : : ;TI`  验证是否每个bulletin都可以证明Pub(Cn) 并且 每个buttin对应的code de vote 都不一样
        
        1. 负责点票的用户`T1,...,TI`  其中一人负责选票的integrite
            1. liste `L` 和 所有的bulletin都有
            2. 每个bulletin都有一个signature，并且这个signature可以证明知道所有`Pub(cn)`中的一个
            3. 每个bulletin对应的code（`Pub(cn)`）各不相同
    - **Phase de dépouillement**
      
        计票需要所有 `T1; : : : ;TI`  的密钥
        
        1. 在 depouillement 前，要先进行audit（`decompte des votes`）
        2. `decompte des votes` 需要全部 负责点票的用户`T1,...,TI` 的密钥 （cle privee）
        3. 解密加密的votes结果，然后算每个参选者的票数（累加）

# 基本类型和 Zp 确认

- Zp和générateur g 的确立
- I ： Small Integer, 存储方式为 JSON Number
- `uuid` ( Universally Unique IDentifier)： 存储方式为 JSON string （a string of `Base58` characters, size >= 14）
  - Base58 characters are: 123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz
- B ： Boolean，存储方式为 JSON boolean
- N，Zq，G ： big Integer，写为10进制的形式，存储方式为 JSON string


# 加密算法
- Liste de codes de vote
    - L=shuffle(Pub(C1),...Pub(Cn))
    - Pub(Cn)=g^s
    - s=KDF(Cn)=PBKDF2(HMAC-SHA256, Cn, Salt, iter, dkLen)

      s=T1||T2||...||T{dklen/hlen}
      
      Ti=F(Cn, Salt, iter, i) = U1 XOR U2 XOR ... XOR U{iter}
      
      U1=HMAC-SHA256(Cn,Salt||INT32BE(i))
      
      U2=HMAC-SHA256(Cn,U1)
      
      ...
      
      U{iter}=HMAC-SHA256(Cn,U{iter-1})
    
- 服务器和用户之间的交流
  
  **对称分组加密Blowfish**
  
  每次加密数据为64位（8个字节）
  
  - 初始化P盒、S盒和子密钥K
  - 扩展密钥
  - 加密
      - 经过16轮循环
  - 解密
- Contenu du bulletin de vote
- Zero-knowledge proof
- 统计选票

    **Crypto-système El Gamal**
    
    - 密钥生成
      - 每个负责唱票的创建一组公/私钥
      - 选择一个私钥：Si
      - 公钥：alpha_i =g   （？？？我觉得是 alpha_i=g^{Si}）
      - 公开alpha_i，p，g作为公钥，保留Si作为私钥

    - 加密
      - 投票者Vn随机选择r，计算C1=g^r
      - 共享秘密：h=alpha_i}^r
      - 计算$C2=Mv*h=Mv{alpha_i}^r
      - 发送$(C1,C2)
    - 解密
      - 计算共享秘密： h=C1^{Si}
      - Mv=C2*h^{-1}
      - **解密多个用户：**
        - alpha是所有alpha的乘积
        - s是所有Si的和
