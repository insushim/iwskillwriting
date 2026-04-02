# Blockchain Development Skill

> 블록체인/Web3 개발 전문가 - 스마트 컨트랙트, DApp, NFT

## Triggers
- "블록체인", "blockchain", "웹3", "Web3"
- "스마트 컨트랙트", "Solidity", "이더리움"
- "NFT", "토큰", "코인"
- "DeFi", "DApp", "탈중앙화"
- "메타마스크", "지갑"

## Capabilities

### 1. 스마트 컨트랙트 (Solidity)

#### ERC-20 토큰
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract MyToken is ERC20, Ownable {
    constructor(uint256 initialSupply) ERC20("MyToken", "MTK") Ownable(msg.sender) {
        _mint(msg.sender, initialSupply * 10 ** decimals());
    }

    function mint(address to, uint256 amount) public onlyOwner {
        _mint(to, amount);
    }

    function burn(uint256 amount) public {
        _burn(msg.sender, amount);
    }
}
```

#### ERC-721 NFT
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract MyNFT is ERC721, ERC721URIStorage, Ownable {
    uint256 private _nextTokenId;
    uint256 public mintPrice = 0.01 ether;
    uint256 public maxSupply = 10000;

    constructor() ERC721("MyNFT", "MNFT") Ownable(msg.sender) {}

    function mint(address to, string memory uri) public payable {
        require(msg.value >= mintPrice, "Insufficient payment");
        require(_nextTokenId < maxSupply, "Max supply reached");

        uint256 tokenId = _nextTokenId++;
        _safeMint(to, tokenId);
        _setTokenURI(tokenId, uri);
    }

    function withdraw() public onlyOwner {
        payable(owner()).transfer(address(this).balance);
    }

    // Override required
    function tokenURI(uint256 tokenId) public view override(ERC721, ERC721URIStorage)
        returns (string memory)
    {
        return super.tokenURI(tokenId);
    }

    function supportsInterface(bytes4 interfaceId) public view override(ERC721, ERC721URIStorage)
        returns (bool)
    {
        return super.supportsInterface(interfaceId);
    }
}
```

### 2. 개발 환경

#### Hardhat 설정
```javascript
// hardhat.config.js
require("@nomicfoundation/hardhat-toolbox");
require("dotenv").config();

module.exports = {
  solidity: {
    version: "0.8.20",
    settings: {
      optimizer: {
        enabled: true,
        runs: 200
      }
    }
  },
  networks: {
    sepolia: {
      url: process.env.SEPOLIA_RPC_URL,
      accounts: [process.env.PRIVATE_KEY]
    },
    mainnet: {
      url: process.env.MAINNET_RPC_URL,
      accounts: [process.env.PRIVATE_KEY]
    }
  },
  etherscan: {
    apiKey: process.env.ETHERSCAN_API_KEY
  }
};
```

#### 배포 스크립트
```javascript
// scripts/deploy.js
const hre = require("hardhat");

async function main() {
  const [deployer] = await hre.ethers.getSigners();
  console.log("Deploying with:", deployer.address);

  const MyToken = await hre.ethers.getContractFactory("MyToken");
  const token = await MyToken.deploy(1000000); // 1M 토큰
  await token.waitForDeployment();

  console.log("Token deployed to:", await token.getAddress());

  // Etherscan 검증
  await hre.run("verify:verify", {
    address: await token.getAddress(),
    constructorArguments: [1000000]
  });
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
```

### 3. 프론트엔드 연동

#### ethers.js
```typescript
import { ethers, BrowserProvider, Contract } from 'ethers';
import MyTokenABI from './abi/MyToken.json';

const CONTRACT_ADDRESS = '0x...';

// 지갑 연결
async function connectWallet() {
  if (!window.ethereum) {
    throw new Error('MetaMask not installed');
  }

  const provider = new BrowserProvider(window.ethereum);
  await provider.send("eth_requestAccounts", []);
  const signer = await provider.getSigner();

  return { provider, signer };
}

// 컨트랙트 인스턴스
async function getContract() {
  const { signer } = await connectWallet();
  return new Contract(CONTRACT_ADDRESS, MyTokenABI, signer);
}

// 토큰 전송
async function transferToken(to: string, amount: string) {
  const contract = await getContract();
  const tx = await contract.transfer(to, ethers.parseEther(amount));
  await tx.wait();
  return tx.hash;
}

// 잔액 조회
async function getBalance(address: string) {
  const contract = await getContract();
  const balance = await contract.balanceOf(address);
  return ethers.formatEther(balance);
}
```

#### wagmi + viem (React)
```typescript
// config.ts
import { createConfig, http } from 'wagmi';
import { mainnet, sepolia } from 'wagmi/chains';
import { injected, metaMask } from 'wagmi/connectors';

export const config = createConfig({
  chains: [mainnet, sepolia],
  connectors: [
    injected(),
    metaMask(),
  ],
  transports: {
    [mainnet.id]: http(),
    [sepolia.id]: http(),
  },
});

// components/ConnectButton.tsx
import { useAccount, useConnect, useDisconnect } from 'wagmi';

export function ConnectButton() {
  const { address, isConnected } = useAccount();
  const { connect, connectors } = useConnect();
  const { disconnect } = useDisconnect();

  if (isConnected) {
    return (
      <div>
        <p>{address}</p>
        <button onClick={() => disconnect()}>Disconnect</button>
      </div>
    );
  }

  return (
    <div>
      {connectors.map((connector) => (
        <button key={connector.id} onClick={() => connect({ connector })}>
          Connect {connector.name}
        </button>
      ))}
    </div>
  );
}
```

### 4. NFT 메타데이터

```json
{
  "name": "My NFT #1",
  "description": "This is my awesome NFT",
  "image": "ipfs://QmXxx.../1.png",
  "attributes": [
    {
      "trait_type": "Background",
      "value": "Blue"
    },
    {
      "trait_type": "Rarity",
      "value": "Legendary"
    },
    {
      "display_type": "number",
      "trait_type": "Generation",
      "value": 1
    }
  ]
}
```

### 5. 테스트

```javascript
// test/MyToken.test.js
const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("MyToken", function () {
  let token;
  let owner;
  let addr1;

  beforeEach(async function () {
    [owner, addr1] = await ethers.getSigners();
    const MyToken = await ethers.getContractFactory("MyToken");
    token = await MyToken.deploy(1000000);
  });

  it("Should assign total supply to owner", async function () {
    const ownerBalance = await token.balanceOf(owner.address);
    expect(await token.totalSupply()).to.equal(ownerBalance);
  });

  it("Should transfer tokens", async function () {
    await token.transfer(addr1.address, 100);
    expect(await token.balanceOf(addr1.address)).to.equal(100);
  });

  it("Should fail if sender doesn't have enough tokens", async function () {
    await expect(
      token.connect(addr1).transfer(owner.address, 1)
    ).to.be.revertedWith("ERC20: transfer amount exceeds balance");
  });
});
```

### 6. 보안 체크리스트

```yaml
security_checks:
  - Reentrancy 방지 (ReentrancyGuard)
  - Overflow/Underflow 방지 (Solidity 0.8+)
  - Access Control 확인
  - 외부 호출 최소화
  - 프론트러닝 방지

audit_tools:
  - Slither (정적 분석)
  - Mythril (심볼릭 실행)
  - Echidna (퍼징)

best_practices:
  - OpenZeppelin 라이브러리 사용
  - 테스트넷 충분히 테스트
  - 컨트랙트 검증 (Etherscan)
  - 멀티시그 지갑 사용
  - 업그레이드 가능한 패턴 고려
```
