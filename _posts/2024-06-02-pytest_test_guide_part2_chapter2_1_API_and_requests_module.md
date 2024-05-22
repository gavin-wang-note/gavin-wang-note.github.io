---
title: 《pytest测试指南》-- 第二章 2-1 API与requests模块介绍
date: 2024-06-02 23:00:00
author: Gavin Wang
img: "/img/pytest/pytest-2.png"
top: false
hide: false
cover: false
coverImg:
password:
theme: flip
toc: true
mathjax: false
summary: 《pytest测试指南》一书 第二章 2-1 API与requests模块介绍
categories:
    - [pytest]
    - [Automation]
tags:
    - pytest
    - Automation
---

在现代技术世界中，API（应用程序编程接口）扮演着至关重要的角色，为构建软件应用和集成多种技术提供了灵活性和利用现成服务的能力，从而在不同的平台和服务之间架起了沟通的桥梁。

在数字化时代，API促进了各种服务和应用的互联互通，无论是通过提高已有服务的可访问性，还是创建基于多个服务的新的应用程序。API使得公司能够开放其服务，扩大业务范围，并与创新者合作，共同创造新的价值。同时，它们也使得个人和企业能够享受到不断进步的技术带来的便利。

# 1.1 什么是API

API（应用程序编程接口，Application Programming Interface）是一套明确定义的方法或协议，用于构建和交互软件应用程序。API允许不同软件系统以一种预先定义的方式相互通信，实现数据和功能的交换。

描述的比较抽象，让人很懵，不好理解。我们可以把它比作一家餐厅的点餐过程，在这个类比中，顾客是用户，菜单是接口（API），服务员则扮演中间人的角色，帮助传达顾客（用户）的需求给厨房（系统或服务）。

想象一下你来到一家名为“代码美食”的餐厅：

* **进入餐厅 — 请求建立**

当你步入餐厅，眼前展开了种类繁多的菜单。这就像是打开了一个API的功能列表，它展示了所有可用的服务和请求类型，就像菜单上展示的各种菜品一样。

* **浏览菜单 — 接口文档查阅**

你坐下来仔细查阅菜单（API文档），并决定点一份“GET汤面”（一种API请求类型，GET请求用来获取资源），就如同开发者查看API文档以了解不同的接口调用和所需要的参数。这个步骤至关重要，因为它决定了你能得到什么样的服务。

* **点餐 — 发送请求**

选择好想吃的菜品后，你告诉服务员（发送一个API请求），请求一份汤面，并且说明，你想要额外的辣椒（一个查询参数）。在API的世界里，这对应于发送一个请求，就像通过互联网将包含你需求的信息发送给服务器一样。

* **服务员确认 — API请求确认**

服务员会确认你的订单，可能会重复你所点的菜品，并询问一些细节，比如你要的面是粗面还是细面，对口感的要求。在API中，这就是请求的确认及对额外信息的询问，这可以通过请求参数或请求头来实现。

服务员记下你的要求，然后走向厨房（系统或服务器），告诉厨师（服务器的处理器）如何按照你的要求准备这碗面。

* **厨师烹饪 — 请求处理和响应**

待服务员将订单交给厨房后，厨师开始烹饪你所点的菜品。外界看不见这个过程，就像服务端接收请求并处理它，而客户端看不到背后的工作。厨师正确理解并执行订单上的指示至关重要，这正如API端准确处理传入的请求一样。

* **上菜 — 得到响应**

过了一会儿，服务员带着满足你请求的汤面（响应）回来了。如果所有一切都按预期进行，汤面将正是你要求的那样（成功的API响应）。如果厨房里发生了什么意外，比如辣椒用完了，服务员会回来通知你问题并提供其他选项（API错误或状态码）。
在API中，这个阶段对应于客户端接收到服务器的响应，通常是JSON或XML格式的数据。

* **品尝以及反馈 — 响应处理和后续动作**

当你品尝到这些美食时，你可能会对这些菜品满意，或者找到一些不尽人意的地方。这时，你可能会给出反馈或者请求改进。类似地，一旦应用程序收到API的响应，它将解析数据，并根据数据的具体内容执行后续任务，或者在有错误时尝试修复或重新发送请求。

<img class="shadow" src="/img/in-post/代码餐厅点餐流程示例.png" width="600">

此“代码美食”虚拟餐厅提供了一个模拟，帮助理解API在软件开发中扮演的中间人角色，它定义了请求服务的方式、请求的种类以及如何处理这些请求的响应。就像你不需要知道厨房是如何工作的来享受美食一样，使用API你也不需要了解服务背后的代码细节来享受服务或数据。

API为软件提供了一个清晰的交流协议，正如菜单、服务员和厨师之间的配合让餐厅能够顺畅地运作。在技术实现中，API确保各个软件组件之间能够通信和交互，它们处理请求、返回数据并执行必要的背景操作，以满足用户的需求。

# 1.2 API的组成

API通常由以下几部分组成

**端点（Endpoints）**：

- 每个API端点代表了一个可供调用的URI（统一资源标识符）。
- 端点通常与软件功能或资源有关联。

**方法（Methods）**：

- HTTP协议中常用的方法有 GET（读取）、POST（创建）、PUT（更新/替换）、PATCH（部分更新）、DELETE（删除）等。
- 这些方法定义了客户端应用程序与服务器之间交换数据的模式。

**请求头（Request Headers）**：

- 包括身份验证信息，如令牌或API密钥。
- 定义了数据的类型（即内容类型），例如：application/json，text/html等。
- 可包含其他客户端希望与服务器通信的信息。

**请求正文（Request Body）**：

- 仅当使用POST、PUT、PATCH等方法时使用。
- 包含发送至 API 端点的数据。

**查询参数（Query Parameters）**：

- 附加在URL末尾，用于提供额外的操作指令，例如搜索、筛选和分页。
- 通常以`?key=value`的格式出现，多个参数时用`&`分隔。

**响应头（Response Headers）**：

- 包含关于响应的信息，如状态码、限制、分页信息等。

**响应正文（Response Body）**：

- 包含请求的结果数据。
- 通常是JSON 或 XML 格式，这由请求头中的 Accept 字段指定。

**状态码（Status Codes）**：

- 表示请求是否成功，并提供错误的情况下的上下文。
- 常见的 HTTP 响应状态码包括200（成功），404（未找到），500（服务器错误）等。

**版本（Versioning）**：

- 为API提供版本，以在不破坏已有用户应用程序的情况下进行更新。
- 通常在API端点的路径中指明，如 `/v1/resource`。

**文档（Documentation）**：

- 提供了API的使用说明，包括每个端点、支持的方法、参数和示例请求/响应。
- 好的文档对于API的可用性至关重要。

**安全（Security）**：

- 保证API安全的机制，如使用HTTPS、OAuth、API密钥、JWT（JSON Web Tokens）等。

**错误处理（Error Handling）**：

- API需要预先定义错误或异常响应，并在遇到问题时提供充足的信息，方便开发者处理。


# 1.3 API的主要特点

* **抽象层**：API为应用程序提供了一个抽象层，使开发者只需了解如何利用API提供的功能，而不需要理解背后的内部实现细节。

* **简化编程**：API简化了编程过程；开发人员可以使用预定义的函数和过程，而不是从头开始写代码，从而提高效率和减少错误。

* **模块性**：API为软件组件提供接口，这使得软件系统可以模块化设计，各个模块之间通过API进行通信。

* **安全性**：合适的API设计可以隐藏系统的内部工作原理，只暴露有限的功能，并且可以通过身份验证机制来控制对API功能的访问。

* **互操作性**：API使不同软件和服务之间能够互通有无。例如，Web API可以允许Web应用程序使用其他应用程序的数据或功能。

* **维护性**：良好设计的API可以保持向后兼容性，当底层系统发生变化时，不会影响到API调用的客户端。

* **可扩展性**：API允许系统扩展新功能，而不干扰现有的系统操作。

* **标准化**：API通常遵循某些标准化的设计原则和协议（如RESTful API使用HTTP和JSON或XML），这使得它们更容易被理解和使用。

* **文档和工具的支持**：良好的API会配备详尽的文档和开发工具（如SDKs、API管理平台），这有助于开发人员快速学习并有效利用API。

* **版本管理**：为了处理功能的增加或变更，API会进行版本管理。这确保了应用程序在API更新时能够平稳过渡或维持稳定性。

* **调用限制**：为了保护资源免遭滥用，API可能会实施调用限制，比如限制在一段时间内允许的请求次数。

* **响应和请求格式**：API定义了请求的构造方式及响应数据的格式，常见格式如JSON和XML。

* **异构环境下的通讯**：API可以支持不同的硬件平台、操作系统或编程语言之间的通讯，实现数据和功能的共享。

# 1.4 API的工作流程

当一个应用程序需要从另一个应用程序（可能是远程服务器上的一个服务）请求数据或功能时，它会发送一个定义良好的请求到服务器的API端。这个请求包括必需的认证、授权信息和参数。API接收请求，进行处理，并且以事先约定的格式返回响应。工作流程通常包括以下步骤：

* **请求发送：** 客户端（例如应用程序或浏览器）向API发送请求。请求通常包括URL（Uniform Resource Locator）和HTTP（Hypertext Transfer Protocol）方法，例如GET、POST、PUT或DELETE。


* **请求路由：** API接收到请求后，根据请求的URL和方法将请求路由到相应的处理程序或功能。

* **数据处理：** API处理请求中的数据，并执行相应的操作。这可以包括从数据库中检索数据、对数据进行计算或处理、调用其他服务或执行其他业务逻辑。

* **数据响应：** API根据处理结果生成响应。响应通常包括HTTP状态码、标头和响应体。响应体可以是包含请求结果的数据，通常是以JSON（JavaScript Object Notation）或XML（eXtensible Markup Language）格式返回。

* **响应发送：** API将生成的响应发送回客户端。响应通过网络传输，并在客户端进行处理。

* **客户端处理：** 客户端接收到API的响应后，根据响应的内容进行处理。这可能涉及数据解析、错误处理、结果展示或其他逻辑操作。

* **循环：** 在应用程序中可能会有多个API请求和响应的循环，直到达到所需的结果或完成特定的业务流程。

API的工作流程可以根据具体的应用程序、协议和需求而有所不同。一些API可能需要身份验证或授权，一些API可能需要处理复杂的业务逻辑，而其他API可能只需要简单地提供数据的读取和写入功能。总体而言，API的工作流程涵盖了请求发送、路由和验证、处理请求、数据处理和操作、生成响应以及响应返回等步骤，以实现应用程序之间的通信和数据交互。

# 1.5 API的分类

API可以根据其功能和使用方式进行分类，以下是几种常见的API分类：

* **Web API：** Web API是一种通过网络协议（如HTTP）提供的API，用于访问和操作远程服务器上的资源。Web API通常以REST（Representational State Transfer）或SOAP（Simple Object Access Protocol）形式提供，用于与Web服务进行通信。

* **Library API：** Library API（也称为SDK，Software Development Kit）是一组函数、类和方法的集合，用于在特定编程语言中访问和使用库的功能。Library API提供了封装的接口，使开发者能够轻松地使用库的功能，而不需要了解其具体实现细节。

* **Operating System API：** 操作系统API是一组函数、方法和工具的集合，用于与操作系统进行交互和访问底层系统资源。操作系统API提供了访问文件系统、网络、设备、进程管理等功能的接口，以便开发者可以编写系统级应用程序和服务。

* **Database API：** 数据库API是一组函数、方法和协议的集合，用于与数据库系统进行交互和操作数据。数据库API提供了连接数据库、查询数据、插入、更新和删除数据等操作的接口，以便开发者可以轻松地进行数据库操作。

* **Third-Party API：** 第三方API是由第三方开发者或组织提供的API，用于访问其特定服务或功能。这些API可以提供访问社交媒体平台、支付网关、地图服务、人工智能服务等功能的接口，以便开发者能够集成和利用这些服务。

* **Hardware API：** 硬件API是一组函数和协议的集合，用于与硬件设备进行通信和控制。这些API提供了访问和操作硬件设备（如传感器、摄像头、打印机等）的接口，以便开发者可以编写与硬件交互的应用程序。

这些是一些常见的API分类，每种类型的API都有其特定的功能和用途。开发者可以根据自己的需求选择适合的API来构建应用程序和系统。

由于本书项目自动化示例所对应的产品，使用的是RESTFul风格的API，会着重介绍一下它。


# 1.6 Web API

Web API（Web Application Programming Interface）是一种通过Web协议（如HTTP）提供服务和资源访问的接口。它允许应用程序通过网络与远程服务器进行通信，并使用服务器上的功能和数据。

Web API的设计和实现通常遵循REST（Representational State Transfer）或SOAP（Simple Object Access Protocol）协议。RESTful API是一种基于REST原则的API，使用HTTP方法（如GET、POST、PUT、DELETE）对资源进行操作。SOAP API则是使用XML来封装和传输数据。

**Web API的主要特点和优点包括：**

* **基于标准协议：** Web API使用标准的Web协议（如HTTP）进行通信，使其能够与各种平台和技术进行集成和交互。
* **跨平台和跨语言：** Web API是基于Web标准的，可以使用任何支持HTTP协议的语言和平台进行访问和使用
* **松耦合性：** Web API提供了独立于实现细节的接口，客户端和服务器之间的耦合度较低，使得系统的不同组件可以独立开发和演化。
* **可扩展性：** Web API可以通过增加新的资源和功能来扩展和改进，而不需要对客户端进行修改。
* **可缓存性：** Web API利用HTTP的缓存机制，可以减少服务器的负载，提高性能和可扩展性。

**Web API的应用非常广泛，包括但不限于以下领域：**

- **社交媒体平台**：Twitter、Facebook、微博、抖音等平台提供API，允许开发者访问用户数据、发布内容和与社交网络进行交互。
- **地图和位置服务：** Google Maps、Baidu Maps等平台提供API，允许开发者在自己的应用程序中集成地图、位置搜索和导航功能。
- **电子商务**：支付网关（如PayPal、支付宝）、商品搜索和推荐服务提供商等平台提供API，允许开发者在自己的电子商务应用中进行支付、商品搜索和推荐。
- **云存储和文件服务：** Amazon S3、阿里云等提供API，允许开发者在自己的应用程序中进行文件上传、下载和存储。
- **媒体和内容分发：** YouTube、新华社、人民日报等提供API，允许开发者在自己的应用程序中集成视频播放和内容分发功能。

## 1.6.1 RESTful API

RESTful API（Representational State Transfer API）是一种基于REST架构风格设计的API。它是一种使用HTTP协议进行通信的Web API，通过HTTP方法（如GET、POST、PUT、DELETE）对资源进行操作。

### 1.6.1.1 RESTful API的设计原则

* **资源（Resources）：** API的核心是资源，每个资源都有唯一的标识符（URI）来访问和操作。
* **统一的接口（Uniform Interface）：** API的接口应该是统一的，使用标准的HTTP方法（GET、POST、PUT、DELETE）来对资源进行操作，使用标准的HTTP状态码来表示操作结果。
* **无状态（Stateless）：** API不应该维护客户端的状态，每次请求都应该包含足够的信息来处理请求，服务器不会保存客户端的状态。
* **超媒体驱动（HATEOAS）：** API应该返回资源之间的关系和可执行操作的链接，客户端可以通过解析这些链接来导航和使用API。

### 1.6.1.2 RESTful API工作流程

* 客户端向服务器发送一个包含HTTP（或HTTPS）请求的请求。
* 服务器对HTTP请求进行解析，并针对该请求执行特定的操作。
* 服务器处理这个请求，并将一个HTTP（或HTTPS）响应返回给客户端。
* 客户端解析该响应，并根据响应的内容采取适当的操作。

更具体地，RESTful API的工作流程如下：

* 客户端向服务器发送预定义的HTTP请求（例如GET、PUT、POST和DELETE等）。
* 服务器验证该请求是否合法，包括验证用户的凭据和请求格式等。
* 如果请求是合法的，服务器将对数据处理请求进行处理。这可能涉及到将数据存储到数据库中，或者从数据库中获取数据以便查找、修改或删除。
* 如果操作成功，服务器将生成一个HTTP响应并根据REST架构原则选择正确的状态码（例如200 OK或201 Created）。
* 服务器将响应返回给客户端。如果请求失败，则包含HTTP错误代码（例如400 Bad Request或500 Internal Server Error）。

如下图所示：

<img class="shadow" src="/img/in-post/RESTFul工作流程.png" width="600">




客户端与RESTful API之间的通信通常涉及JSON或XML等标准数据格式的使用。客户端将责任分配给RESTful API以管理数据，以便在数据的转移和交换过程中保持一致性和完整性。

### 1.6.1.3 RESTful API的优点

* **可扩展性：** 由于RESTful API使用标准的HTTP方法和状态码，它可以与不同的客户端和服务器进行交互，并且可以轻松地扩展和修改。
* **可读性和可理解性：** RESTful API的URI和HTTP方法具有自解释性，使得开发者和用户可以直观地理解和使用API。
* **松耦合性：** RESTful API的无状态性和统一接口减少了客户端和服务器之间的依赖，使得系统的组件可以独立开发和演化。
* **缓存支持：** RESTful API利用HTTP的缓存机制，可以有效地减少服务器的负载，提高性能和可扩展性。

### 1.6.1.4 API示例

针对上文“代码美食”虚拟餐厅，根据RESTful风格，我们再来丰富一下它的API。

**菜单服务API示例**

- 获取菜单信息：
  - 请求方式：GET
  - URL：`https://api.codefood.com/menu`
  - 响应：返回包含菜单信息的JSON数据

- 获取特定菜品信息：
  - 请求方式：GET
  - URL：`https://api.codefood.com/menu/dishes/{dish_id}`
  - 响应：返回特定菜品的详细信息的JSON数据

- 创建新菜品：
  - 请求方式：POST
  - URL：`https://api.codefood.com/menu/dishes`
  - 请求体：包含新菜品信息的JSON数据
  - 响应：返回创建成功或失败的菜品的JSON数据

   - 更新菜品信息
     * 请求方式：PUT
     * URL：`https://api.codefood.com/menu/{dish_id}`
     * 请求体：包含菜品更新信息的JSON数据
     * 响应：返回更新菜品成功或失败的JSON数据
   - 删除菜品
     - 请求方式：DELETE
     - URL： `https://api.codefood.com/menu/{dish_id}`
     - 请求体：包含被删除菜品信息的JSON数据
     - 响应：返回被删除菜品的删除成功或失败的JSON数据

**服务员服务API示例**：

- 创建订单：
  - 请求方式：POST
  - URL：`https://api.codefood.com/waiter/orders`
  - 请求体：包含订单信息的JSON数据
  - 响应：返回创建成功的订单的JSON数据

- 更新订单状态：
  - 请求方式：PUT
  - URL：`https://api.codefood.com/waiter/orders/{order_id}`
  - 请求体：包含要更新的订单状态的JSON数据
  - 响应：返回更新后的订单的JSON数据

- 获取特定订单信息：
  - 请求方式：GET
  - URL：`https://api.codefood.com/waiter/orders/{order_id}`
  - 响应：返回特定订单的详细信息的JSON数据

- 提供服务员建议
  - 请求方式：GET
  - URL： `https://api.codefood.com/waiter/orders/{order_id}/suggestions`
  - 响应：返回特定订单的建议发送结果

通过这些请求和响应，客户端（顾客）可以与服务器（厨房）进行交互，实现对用户数据（菜单）的增删改查等操作。

## 1.6.2 SOAP API

SOAP（Simple Object Access Protocol）API是一种基于XML的通信协议，用于在网络上进行应用程序之间的交互。与RESTful API不同，SOAP API使用SOAP协议来定义消息格式和通信规范。

### 1.6.2.1 SOAP API的设计原则

* 所有SOAP请求和响应都是XML格式，使得SOAP可以独立于任何特定的语言以及操作系统。
* SOAP协议的目标是在不同的系统之间进行通信，因此它的方法和建议的编码标准非常具体。
* SOAP协议具有明确定义的错误和异常处理机制，可以确保无论何时出现问题，都可以清晰地将问题追踪到根源。
* SOAP API具有广泛的支持，几乎可以与任何语言和平台无缝集成。
* SOAP消息通常需要签名和验证，确保消息的完整性和安全性。
* SOAP API非常适合进行分布式系统之间的通信。

### 1.6.2.2 SOAP API工作流程

* **定义接口**：首先，定义SOAP API的接口，包括可用的方法、参数和返回类型等。这通常使用WSDL（Web Services Description Language）文件来描述。
* **生成客户端和服务端代码**：根据定义的接口，使用SOAP工具集生成客户端和服务端的代码。这些代码用于处理SOAP消息的创建、解析和处理。
* **创建SOAP消息**：客户端创建包含请求数据的SOAP消息，并将其发送到目标服务端。SOAP消息由SOAP Envelope、SOAP Header和SOAP Body组成。
* **发送SOAP消息**：客户端将SOAP消息通过网络发送到目标服务端，通常是通过HTTP协议进行传输。
* **处理SOAP消息**：服务端接收到SOAP消息后，解析消息并执行相应的操作。服务端将生成包含响应数据的SOAP消息，并将其发送回客户端。
* **解析和处理响应**：客户端接收到服务端的响应SOAP消息后，解析消息并处理响应数据。客户端根据需要提取所需的信息，并执行相应的操作。

### 1.6.2.3 SOAP API的优缺点

**优点：**

* 独立于平台和语言，具有良好的可扩展性，兼容性和协调性。
* 明确定义的错误和异常处理机制可以提高开发人员的开发效率。
* SOAP具有非常广泛的支持，并且可以与任何语言和平台无缝集成。
* SOAP可以通过使用WS-Security保护数据的完整性和安全性。
* SOAP API非常适合进行分布式系统之间的通信。

**缺点：**

* SOAP消息体积通常比REST大很多，因为它需要使用XML文件描述数据。
* SOAP API有明确的规范和要求，这可能会限制开发人员在开发API上的灵活性。
* 由于SOAP API使用了严格的描述性语言，因此它的可读性和理解性可能会比REST稍低一些。
* SOAP API的启动时间可能会比REST慢，因为SOAP需要建立网络连接。此外，SOAP操作的复杂性可能导致性能问题。

### 1.6.2.4 API 示例

下面是一个简单的SOAP API示例代码：

```xml
<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope 
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
    xmlns:xsd="http://www.w3.org/2001/XMLSchema" 
    xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
    <soap:Body>
        <GetCitiesByCountry xmlns="http://www.webserviceX.NET">
            <CountryName>China</CountryName>
        </GetCitiesByCountry>
    </soap:Body>
</soap:Envelope>
```

在此示例中，请求的内容是“GetCitiesByCountry”方法的调用，使用了“CountryName”参数作为请求。该请求遵循SOAP的规范，并使用XML作为请求和响应数据的格式。通过使用这种协议，不同的系统可以使用各自的编程语言，并使用支持SOAP协议的API进行通信。



SOAP API在企业级应用程序中广泛使用，特别适用于复杂的系统集成和数据交换。它提供了一种可靠且功能强大的方式来实现应用程序之间的通信和数据交互。然而，由于SOAP的复杂性和较大的消息体积，它相对于RESTful API来说更重量级，可能在性能和灵活性方面存在一些限制。因此，在选择API时，需要根据具体的需求和应用场景来综合考虑。

## 1.6.3 GraphQL API

GraphQL API 是一种用于查询和操作数据的 API，它使用一种称为 GraphQL 的查询语言。GraphQL API 的主要优点是它允许客户端只请求所需的数据，从而减少了网络流量和提高了性能。

### 1.6.3.1 GraphQL API的设计原则

* **单一端点：** GraphQL API只有一个端点，通过该端点发送所有的查询请求，减少了网络请求的次数。

* **精确数据获取：** 客户端可以精确指定需要获取的字段和关联关系，避免了过度获取或不足的问题。

* **强类型系统：** GraphQL具有强大的类型系统，定义了可用的类型、字段和关联关系，使得API的结构和数据类型更加清晰和可靠。

* **自省能力：** GraphQL具有自省能力，客户端可以查询服务器上可用的类型和字段，使得客户端可以动态构建查询并且不需要事先了解服务器上的数据结构。

GraphQL 查询语言是一种声明式语言，这意味着它只描述客户端想要的数据，而不指定如何获取数据。这使得 GraphQL API 非常灵活，因为它可以用于查询各种不同的数据源，包括关系型数据库、非关系型数据库和 REST API。

### 1.6.3.2 GraphQL API的优缺点

**优点：**

* **精确获取数据：** 客户端可以根据自身需求精确获取所需的数据，避免了过度获取和不足的问题，提高了数据传输的效率。

* **减少网络请求：** 由于只有一个端点，客户端可以在一个请求中获取多个资源，减少了网络请求的次数，提高了性能。

* **强大的类型系统：** GraphQL具有强大的类型系统，使得API的结构和数据类型更加清晰和可靠，减少了出现错误的可能性。

* **自省能力：** GraphQL的自省能力使得客户端可以动态构建查询，不需要事先了解服务器上的数据结构，提高了开发的灵活性和效率。

**缺点：**

* **学习成本较高：** 相比于传统的RESTful API，使用GraphQL需要对其查询语言和类型系统有一定的了解，增加了学习和理解的成本。

* **缓存支持较弱：** 由于每个请求都可以具有不同的查询字段，缓存对GraphQL的支持较弱，需要额外的处理来实现缓存。

* **缺乏标准化：** GraphQL并没有像RESTful API那样有一套标准化的规范，因此在实践中可能存在一些差异和实现细节的差异。

### 1.6.3.3 API 示例

假设有一个图书管理系统，其中有图书和作者两个资源。使用GraphQL API设计可以如下：

```graphql
type Book {
  id: ID!
  title: String!
  author: Author!
}

type Author {
  id: ID!
  name: String!
  books: [Book!]!
}

type Query {
  book(id: ID!): Book
  author(id: ID!): Author
  books: [Book!]!
  authors: [Author!]!
}
```

客户端可以发送如下查询来获取图书和作者的信息：

```graphql
# 获取所有图书
query {
  books {
    id
    title
    author {
      id
      name
    }
  }
}

# 获取特定图书和作者
query {
  book(id: "1") {
    id
    title
    author {
      id
      name
    }
  }
}

# 获取所有作者
query {
  authors {
    id
    name
    books {
      id
      title
    }
  }
}
```

通过GraphQL API设计，客户端可以根据自身的需求精确获取所需的数据，如获取特定图书的信息、获取某个作者的所有图书列表等。同时，客户端还可以通过Mutation进行数据的创建、更新和删除操作，保持与图书管理系统的数据同步。这样，使用GraphQL API可以更灵活、高效地管理图书和作者的数据。

### 1.6.3.4 GraphQL API 的未来

GraphQL API 是一种非常有前途的 API 技术，它有望在未来几年内变得更加流行。随着 GraphQL API 工具支持的完善和社区规模的扩大，GraphQL API 将成为构建现代 Web 应用程序的首选 API 技术之一。



# 1.7 认证与授权之Cookie、Session、Token、JWT

## 1.7.1 认证与授权

认证和授权是在网络应用中常见的安全机制，用于确保用户的身份验证和访问权限控制。

### 1.7.1.1 认证

**认证**（Authentication）是验证用户身份的过程，确保用户是其声称的身份。认证通常涉及用户提供凭据（如用户名和密码）来验证其身份。认证的目的是确认用户是合法用户，并允许他们访问受保护的资源。

常见的认证方式包括：

- 用户名和密码认证：用户提供用户名和密码进行验证。
- 社交登录认证：使用第三方身份提供者（如Google、Facebook）验证用户身份。
- 双因素认证：结合密码和其他验证因素（如手机验证码）进行身份验证。
- 数字证书认证：使用数字证书验证用户身份。
- 生物识别认证：使用指纹、面部识别等生物特征进行身份验证。

### 1.7.1.2 授权

**授权**（Authorization）是确定用户在系统中所具备的权限和访问权限的过程。一旦用户通过认证，授权机制将决定用户能够访问哪些资源和执行哪些操作。授权的目的是保护资源免受未经授权的访问和操作。

常见的授权方式包括：

- 基于角色的访问控制（Role-Based Access Control，RBAC）：将用户分配到不同的角色，并为每个角色分配特定的权限。
- 基于属性的访问控制（Attribute-Based Access Control，ABAC）：基于用户属性、环境条件和资源属性来控制访问。
- 基于策略的访问控制（Policy-Based Access Control，PBAC）：使用事先定义的策略来确定对资源的访问权限。
- 细粒度访问控制（Fine-Grained Access Control）：对每个资源和操作进行精细的控制，以确保最小权限原则。

### 1.7.1.3 认证与授权的关系和区别

尽管认证和授权通常一起使用，但它们解决了访问控制的两个不同方面：

- **认证**确定用户是谁，并不提供任何关于用户能做什么的信息。
- **授权**确定认证用户可以进行的操作，依赖于认证过程的结果来授予权限。

在实际应用中，认证和授权通常是一起使用的，认证通常是访问控制流程的第一步，一旦用户成功认证，系统才会进行授权检查来决定用户能够访问的服务或资源范围。这种安全机制能够确保只有经过认证和授权的用户才能够访问受保护的资源，从而保障系统的安全性和数据的完整性。例如，在Web应用程序中，用户首先需要进行登录（认证），然后应用根据用户的角色和权限（授权）来允许或拒绝对特定部分的访问。



## 1.7.2 授权实现方式

### 1.7.2.1 Cookie

Cookie是客户端的一种数据存储机制。服务器在响应请求时，可以将一些数据存储在Cookie中，并通过响应的头部将Cookie发送给客户端保存。客户端在后续的请求中会自动携带该Cookie，将存储的数据发送给服务器。Cookie通常用于存储一些简单的键值对数据，如用户的偏好设置、跟踪用户的行为等。客户端可以通过JavaScript或服务器端代码来读取和操作Cookie的值。

Cookie的特点：

- 存储在客户端（浏览器）。
- 有大小限制（通常是4KB）。
- 每个域名下存放的Cookie数量有限制。
- 有过期时间，可以设置为会话Cookie（关闭浏览器时失效）或持久Cookie（在一个设定的过期日期之后才会失效）。
- 通过HTTP头传输，因此除了在浏览器上的大小和数量限制，过量使用也可能影响网站的性能。

Cookie 工作流程示意图：

<img class="shadow" src="/img/in-post/cookie工作流程示意图.png" width="600">

* 浏览器向服务器发送请求；
* 服务器响应请求，向浏览器设置 cookie；
* 浏览器将 cookie 存在本地，下一次请求带上该 cookie；
* 服务器响应请求。

### 1.7.2.2 Session

Session是服务器端的一种状态管理机制。当用户访问一个网站时，服务器会为该用户创建一个唯一的会话，并为该会话分配一个唯一的Session  ID。服务器会将Session  ID存储在Cookie中，然后将Cookie发送给客户端保存。客户端在后续的请求中会自动携带该Cookie，服务器可以根据Session  ID来识别用户并获取相关的会话数据。服务器端会将会话数据保存在服务器上，通常可以存储在内存、数据库或文件系统中。Session可以存储用户的登录状态、购物车内容等信息，用于实现用户的个性化体验。

Session的特点：

- 存储在服务器端。
- 存储数据量大小一般由服务器内存和资源决定。
- 为每个用户创建一个唯一的Session ID。
- 更安全，因为数据不是通过每次HTTP请求传递的，用户无法直接访问存储的信息。

Session工作示意图：

以用户login和logout为示例，流程图参考如下：



<img class="shadow" src="/img/in-post/login_logout流程图.png" width="600">

* 首次请求时，服务端接收客户端传来的用户名和密码等信息，进行登录认证，服务器根据用户提交的信息进行鉴权，鉴权成功后创建 session 对象，并将 session ID塞入 cookie 中，浏览器收到响应信息将 cookie 存入本地。
* 再次请求时，浏览器自动将当前域名下的 cookie 信息发送给服务端，服务端解析 cookie，获取到 session ID后再查找对应的 session 对象，如果 session 对象存在说明用户已经登录，进而可以继续操作。
* 当用户退出系统或 session 过期销毁时，客户端的 session_id 也就无效了。

从上面的流程可知，session ID是 cookie 和 session 中间的一道桥梁：

* session 由服务端产生；
* 以字典的形式存储，session 保存状态信息，session ID返回给客户端保存至本地；
* 服务端需要一定的空间存储 session，且一般为了提高响应速度，都是存储在内存中；
* session ID会自动由浏览器带上。

### 1.7.2.3 cookie与session的区别

在Web开发中，Cookie和Session通常结合使用。例如，Session可以用来存储用户的登录信息，而Session  ID则是通过Cookie传递给用户浏览器的。这样，服务器就能在用户的每次请求中识别出用户，并提供相应的服务。然而，也存在用户禁用Cookie的情况，此时可以通过URL重写等技术来传递Session ID。

Cookie 和 Session 都是用来跟踪浏览器用户身份的会话方式，但是两者的应用场景不太一样。两者的区别如下表所示：

| 特性       | Session（会话）                       | Cookie（小型文本文件）                           |
| ---------- | ------------------------------------- | ------------------------------------------------ |
| 定义       | 服务器端的状态管理机制                | 客户端的数据存储机制                             |
| 存储位置   | 服务器端                              | 客户端浏览器                                     |
| 生命周期   | 通常由服务器设置，会话结束时失效      | 由开发者设定，可以是持久的                       |
| 存储容量   | 较大，受服务器内存限制                | 较小，单个cookie的大小限制（一般为4KB）          |
| 安全性     | 较高，因信息存储在服务器              | 较低，因信息存储在客户端，易于拦截和篡改         |
| 目的       | 管理服务器与用户之间的会话状态        | 存储用户偏好、追踪会话等客户端信息               |
| 带宽影响   | 小，每次HTTP请求不需要传输session信息 | 较大，每次HTTP请求都可能携带cookie信息           |
| 适用性     | 对象存储，如登录信息、购物车等        | 文本数据存储，如用户识别、站点设置               |
| 影响速度   | 对服务器性能有影响但不影响网络速度    | 大量使用可增加请求大小，影响加载速度             |
| 跨域访问   | 不易实现                              | 可以设置支持跨域访问                             |
| 依赖关系   | 可以利用cookie来存储会话标识符        | 独立存在，但可被session利用                      |
| 生命周期   | 通常持续时间较长，可以设置过期时间    | 可以设置过期时间，可以是会话级别或持久性         |
| 客户端支持 | 不依赖于客户端的支持                  | 需要客户端（浏览器）的支持，可以通过脚本进行操作 |

### 1.7.2.4 token

Token是一种在Web开发中常用的身份验证和授权机制，它是一串由服务器生成的随机字符串，用于识别用户的身份和权限。

Token的主要作用是实现无状态的身份验证和授权。传统的身份验证方式通常使用基于会话（Session）的机制，服务器在验证用户身份后会为用户创建一个会话，并将会话信息存储在服务器端。但这种方式需要在服务器端维护会话状态，对于分布式系统或高并发环境来说，会增加服务器的负担和复杂性。

而Token机制通过在用户登录后生成一个Token，并将Token发送给客户端保存，客户端在后续的请求中携带该Token。服务器在接收到请求时，通过验证Token的有效性和权限，来判断用户的身份和权限。

Token的使用有以下几个优点：

* **无状态性：** 服务器不需要在后端存储用户的会话信息，不需要维护会话状态。每个请求都是独立的，可以在不同的服务器之间进行负载均衡或水平扩展。
* **可扩展性：** Token机制适用于分布式系统或多个服务之间的身份验证和授权。不同的服务可以共享同一个Token验证机制，实现统一的身份验证和权限控制。
* **安全性：** Token可以包含加密的信息，如用户ID、角色、过期时间等。服务器可以通过对Token进行解密和验证，来确保Token的有效性和安全性。
* **灵活性：** Token可以用于不同的身份验证和授权场景，如API访问、单点登录、跨域认证等。它可以与不同的身份验证协议（如OAuth、JWT等）结合使用，提供更灵活和安全的身份验证和授权机制。

Oauth2.0 引入了 Access Token 和 refresh token 机制，接下来分别介绍一下它们。

#### 1.7.2.4.1 Access Token

Token工作示意图:


<img class="shadow" src="/img/in-post/access token工作流程.png" width="600">



* 客户端向授权服务器请求Access Token（整个认证授权的流程，可以是多次请求完成该步骤）。
* 授权服务器验证客户端身份无误，且请求的资源是合理的，则颁发Access Token 和 Refresh Token，可以同时返回Access Token的过期时间等附加属性。
* 带着Access Token请求资源。
* 资源服务器验证Access Token有效则返回请求的内容。

**需要注意：**

* 服务器在首次处理用户名和密码时会生成 access token，考虑到安全性，它有一定的有效期，过期后需要依赖 refresh token 来刷新 access token。

* 每次请求都需要携带 access token，需要把 access token 放到 HTTP 的 Header 里。



#### 1.7.2.4.2 Refresh Token

Oauth2.0 引入了 refresh token 机制。当鉴权服务器发送 access token 给使用方时，同时也发送一个 refresh token。 这个 refresh token 的有效期很长，作用是可以用来刷新 access token。

如果没有 refresh token，也可以刷新 access token，但每次刷新都要用户输入登录用户名与密码，会很麻烦。有了 refresh token，可以减少这个麻烦，客户端直接用 refresh token 去更新 access token，无需用户进行额外的操作。

refresh token 工作流程示意图：



<img class="shadow" src="/img/in-post/refresh token 工作流.png" width="600">

这个图表描述了OAuth授权流程的关键步骤，包括获取访问令牌、使用令牌访问资源、处理令牌失效的情况以及刷新令牌的过程。相较于 Access Token 的流程多了下面这些步骤：

- (E) **注意：** 上面的(C)(D)步骤可以反复进行，直到Access Token过期。 如果客户端在请求之前就能判断Access Token已过期或临近过期（下发过期时间），就可以直接跳到步骤(G)。否则，就会再请求一次，也就产生了本步骤。
- (F) 当Access Token无效的时候，资源服务器会拒绝响应资源并返回Token无效的错误。
- (G) 客户端重新向授权服务器请求Access Token，但是这次只需带着Refresh Token即可，而不需要用户再执行认证和授权的流程。这样就可以做到用户无感。
- (H) 授权服务器验证Refresh Token，如果有效，则签发新的Access Token（或者同时下发一个新的Refresh Token）。



#### 1.7.2.4.3 token和session区别

| 类别       | Session              | Token                            |
| ---------- | -------------------- | -------------------------------- |
| 存储位置   | 服务器端             | 客户端                           |
| 状态管理   | 服务器端管理会话状态 | 无状态，不需要在服务器端存储状态 |
| 数据存储   | 存储在服务器内存中   | 存储在客户端                     |
| 安全性     | 高（仅服务器端）     | 低（仅依赖于加密算法和传输方式） |
| 生命周期   | 可设置               | 可设置，通常有过期时间           |
| 性能       | 需要服务器内存和处理 | 无额外服务器开销                 |
| 传输方式   | 通过Cookie传输       | 通过请求头或请求参数传输         |
| 扩展性     | 有限                 | 良好                             |
| 客户端支持 | 不需要客户端支持     | 需要客户端支持                   |
| 用途       | 适用于Web应用程序    | 适用于分布式系统和API            |



###  1.7.2.5 JWT

**JWT（JSON Web Token）** 是一种用于在网络应用间安全传递信息的开放标准（RFC 7519）。它通过使用数字签名或加密算法，将声明式的JSON对象作为安全令牌进行传输。JWT通常用于身份验证和授权，以及在不同系统之间传递声明性信息。

#### 1.7.2.5.1 JWT的结构

一个JWT实际上由三部分构成，它们之间用点（`.`）分隔开来，具体如下：

**Header（头部）**:
Header通常由两部分组成：token的类型（即JWT）和使用的签名算法，如HMAC SHA256或RSA等。这些信息被编码为JSON格式，并使用Base64Url标准转换为字符串。

示例JSON Header:

```json
{
  "alg": "HS256",
  "typ": "JWT"
}
```

经过Base64Url编码后的JWT Header可能看起来如下：

```shell
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9
```

**Payload（负载）**:
负载部分包含所谓的claims（声明）。Claims是关于实体（通常是用户）和其他数据的陈述。有三种类型的claims：注册的claims、公共的claims和私有的claims。

- **注册的claims**: 这些是预定义的claims，不是必须的但是推荐使用，例如：`iss` (issuer，发行者), `exp` (expiration time，过期时间), `sub` (subject，主题), `aud` (audience，听众等。
- **公共的claims**: 可以自由定义的。
- **私有的claims**: 用于在同意使用它们的各方之间共享信息，是自定义的claims。

示例JSON Payload:

```json
{
  "sub": "1234567890",
  "name": "John Doe",
  "admin": true
}
```

经过Base64Url编码后的JWT Payload可能看起来如下：

```shell
eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiYWRtaW4iOnRydWV9
```

**Signature（签名）**:
使用编码的header、编码的payload、一个秘钥，以header中指定的算法进行签名。签名的用途是验证消息在传递过程中没有被篡改，以及对于使用私钥签名的token，验证JWT的发行者是可信的。

Signature示例：

```python
HMACSHA256(
  base64UrlEncode(header) + "." +
  base64UrlEncode(payload),
  secret)
```

完整的JWT看起来像这样：

```shell
xxxxx.yyyyy.zzzzz
```

比如：

```shell
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c
```

#### 1.7.2.5.2 JWT的工作流程

* 用户通过提供有效的凭证（如用户名和密码）进行身份验证。
* 服务器验证凭证，并生成一个JWT作为响应返回给客户端。
* 客户端在后续的请求中使用JWT来证明其身份。JWT通常通过在请求的Authorization头部中添加`Bearer`前缀进行传递。
* 服务器接收到请求后，校验JWT的签名并解析Payload中的声明信息，以验证请求的合法性和对应的权限。

如下图所示：


<img class="shadow" src="/img/in-post/JWT工作流程图.png" width="600">

#### 1.7.2.5.3 JWT的优点和特点包括

- **轻量且自包含**：JWT是一个紧凑的字符串，可以轻松地在网络上进行传输，并且包含了自身所需的所有信息。

- **无状态**：由于JWT包含了所有必要的信息，服务器不需要在后端存储会话信息，因此可以实现无状态的身份验证和授权。

- **可扩展性**：JWT的Payload可以包含自定义的声明信息，使其具有良好的可扩展性。

- **安全性**：JWT使用数字签名或加密算法来验证数据的完整性和安全性，防止数据在传输过程中被篡改。

- **跨域支持**：JWT可以在不同的域之间进行传递和共享，使得它非常适用于分布式系统和服务之间的通信。

需要注意的是，JWT是基于客户端的可信任性，因为其中包含了用户的身份信息。因此，在使用JWT时，需要采取适当的安全措施来保护令牌的机密性和完整性。

#### 1.7.2.5.4 JWT的一些注意事项

- 因为JWT的payload编码而不是加密，所以不应该在payload中放置任何敏感信息，除非它是加密的。
- JWT不适合所有的场景，特别是那些需要token吊销的场景，JWT是无状态的。
- 必须通过HTTPS传输JWT，防止中间人攻击。



# 1.8 API测试

接口测试通常是指API测试。在软件开发领域，接口测试是一种软件测试，旨在验证应用程序接口的功能、可靠性、性能和安全性。而API（Application Programming Interface，应用程序编程接口）是软件系统中不同组件间通信的规定，因此，当我们谈论接口测试时，我们通常是在讨论针对这些APIs的测试。

API测试关注以下几个关键方面：

- **功能测试**：确认API按预期提供功能服务，包括请求和响应的正确性。
- **可靠性测试**：确保API能在多种条件和高压力环境下坚持运行。
- **性能测试**：评估API的响应时间，以及在高流量下的表现。
- **安全性测试**：检查API是否有潜在的安全问题，如未经授权的数据访问或SQL注入等。

API测试通常通过发送请求到API并验证响应（包含数据和状态码等）来执行。这个过程可以手动完成，也可以通过使用自动化工具，如Postman、REST-assured、SoapUI等，以及使用代码驱动的测试框架，如pytest结合requests库来实现。

接下来重点介绍python的requests库，在介绍之前，简单介绍一下HTTP请求方法和状态码。



## 1.8.1 HTTP 请求方法

如下表所示：


| 方法    | 描述                                                         | 使用场景                                                     | 身体   | 幂等性 | 可缓存 |
| ------- | ------------------------------------------------------------ | ------------------------------------------------------------ | ------ | ------ | ------ |
| GET     | 请求指定的资源。通常用于检索信息。                           | 读取服务器上的数据，不应当有副作用，如刷新页面或链接。       | 否     | 是     | 是     |
| POST    | 向指定资源提交数据进行处理。数据包含在请求体中。可能会导致新的资源的创建或现有资源的修改。 | 提交表单数据，上传文件，创建新资源。                         | 是     | 否     | 否     |
| PUT     | 用于替换指定的资源的所有当前表示。                           | 更新现有资源的完整内容（例如，更新完整的用户资料）。         | 是     | 是     | 否     |
| DELETE  | 用于删除指定的资源。                                         | 删除资源。                                                   | 否     | 是     | 否     |
| OPTIONS | 用于描述目标资源的通信选项。                                 | 用于确定服务器支持的HTTP方法，或CORS预检请求中了解服务器支持的功能。 | 否     | 是     | 否     |
| HEAD    | 与GET方法相似，但无响应体。用于获取资源的元信息而不是资源本身。 | 在不获取资源的情况下检查资源的有效性，可用性，或者最近的修改日期。 | 否     | 是     | 是     |
| PATCH   | 用于对资源进行部分修改。                                     | 对资源进行部分更新，例如修改一篇文章的标题，不需要更新整个文章。 | 是     | 否     | 否     |
| TRACE   | 回显服务器收到的请求，主要用于测试或诊断。                   | 用于诊断信息，跟踪请求-响应链。                              | 否     | 是     | 否     |
| CONNECT | 建立起隧道至服务器由URL指定的资源。                          | 用于代理服务器，以开启到其他网络服务的双向通信。             | 依情况 | 否     | 否     |

**请注意：**

* **遵循REST原则：** 每一种HTTP方法都有其特定的使用场景，遵循REST原则时应当合理地选择相应的方法。例如，`GET` 用于获取资源，`POST` 用于创建资源，`PUT` 用于更新已有资源的状态或创建指定URI的资源，`DELETE` 用于删除资源。而 `OPTIONS` 方法通常被用于跨域请求的预检（preflight），用来检查服务器支持的HTTP方法，以及CORS（跨源资源共享）设置。
* **幂等性（Idempotence）：** 这意味着执行多次与执行一次具有同样的副作用；例如，无论调用几次 `DELETE` 请求，资源只会被删除一次，因此它是幂等的。
* **可缓存性（Cacheable）：** 某个请求的响应是可以被缓存的；例如，多次调用 `GET` 请求并不会改变响应，因此它是可缓存的。而 `POST` 请求可能每次都创建新资源，因此不可缓存。



## 1.8.2 HTTP状态码

当用户与服务器进行HTTP通信时，服务器会返回一个状态码来指示请求的处理结果。HTTP状态码由三位数字组成，分为五个类别，每个类别有特定的含义。下表是HTTP状态码的详细介绍：

| 状态码 | 类别         | 含义                         | 示例代码                    |
| ------ | ------------ | ---------------------------- | --------------------------- |
| 1xx    | 信息类       | 请求已被接收，需要进一步处理 | 无                          |
| 2xx    | 成功类       | 请求已成功处理               | `200 OK`                    |
| 3xx    | 重定向类     | 需要进一步操作以完成请求     | `301 Moved Permanently`     |
| 4xx    | 客户端错误类 | 客户端发送的请求有错误       | `404 Not Found`             |
| 5xx    | 服务器错误类 | 服务器在处理请求时出现错误   | `500 Internal Server Error` |

* 信息类（1xx）：指示服务器已接收请求并正在处理。常见的信息类状态码有：

  - 100 Continue：服务器已接收到请求的初始部分，客户端应继续发送剩余的请求。
  - 101 Switching Protocols：服务器已理解客户端的请求，并将切换到不同的协议。

* 成功类（2xx）：指示请求已成功处理。常见的成功类状态码有：

  - 200 OK：请求成功，服务器返回所请求的数据。
  - 201 Created：请求已成功处理，并在服务器上创建了新的资源。

* 重定向类（3xx）：指示客户端需要执行额外的操作来完成请求。常见的重定向类状态码有：

  - 301 Moved Permanently：请求的资源已永久移动到新位置。
  - 302 Found：请求的资源暂时移动到新位置。

* 客户端错误类（4xx）：指示客户端发送的请求有错误。常见的客户端错误类状态码有：
  - 400 Bad Request：请求有语法错误，服务器无法理解。
  - 404 Not Found：请求的资源不存在。

* 服务器错误类（5xx）：指示服务器在处理请求时出现错误。常见的服务器错误类状态码有：
  - 500 Internal Server Error：服务器在执行请求时发生了不可预料的错误。
  - 503 Service Unavailable：服务器暂时无法处理请求，通常是由于超负荷或维护。

## 1.8.3 Python的requests库介绍

Python的requests库是一个简单、易于使用的HTTP请求库，它提供了各种方法来发送HTTP请求并处理响应。下面将详细介绍requests库中常用的HTTP方法的使用，并提供相应的示例代码和注解。

使用`requests`库时需要安装它，通常可以使用pip进行安装：

```shell
pip install requests
```

### 1.8.3.1 GET请求

```python
# content of get_request.py
import requests

# 发出GET请求，获取资源
response = requests.get('https://jsonplaceholder.typicode.com/posts')
# response.json() 将返回请求的内容
print(response.json())
```

你可以使用 `params` 关键字参数将一个字典传递给 GET 请求，Requests 会自动将参数编码为URL字符串：

```python
params = {'key1': 'value1', 'key2': 'value2'}
response = requests.get('https://jsonplaceholder.typicode.com/posts', params=params)
```

### 1.8.3.2 POST请求

Requests 支持发送请求体数据，适用于POST、PUT等请求方法。

```python
# content of post_request.py
import requests

# 发出POST请求，创建资源
data = {'title': 'foo', 'body': 'bar', 'userId': 1}
response = requests.post('https://jsonplaceholder.typicode.com/posts', data=data)
# response.json() 将返回新创建的资源的内容
print(response.json())
```

`data`参数常用于发送表单数据，也可以使用`json`参数发送JSON数据

```python
# 发送JSON数据
json = {'title': 'foo', 'body': 'bar', 'userId': 1}
response = requests.post('https://jsonplaceholder.typicode.com/posts', json=json)
```

### 1.8.3.3 PUT请求

```python
# content of put_request.py
import requests

# 发出PUT请求，替换/更新整个资源
data = {'id': 1, 'title': 'foo', 'body': 'bar', 'userId': 1}
response = requests.put('https://jsonplaceholder.typicode.com/posts/1', data=data)
# response.json() 将返回更新后的资源内容
print(response.json())
```

### 1.8.3.4 PATCH请求

```python
# content of patch_request.py
import requests

# 发出PATCH请求，部分修改资源
data = {'title': 'foo updated'}
response = requests.patch('https://jsonplaceholder.typicode.com/posts/1', data=data)
# response.json() 将返回更新的资源部分
print(response.json())
```

### 1.8.3.4 DELETE请求

```python
# content of delete_request.py
import requests

# 发出DELETE请求，删除资源
response = requests.delete('https://jsonplaceholder.typicode.com/posts/1')
# response.status_code 应为200，表示成功删除，无返回内容
print(response.status_code)
```

### 1.8.3.5 HEAD请求

```python
# content of head_request.py
import requests

# 发出HEAD请求，获取资源的元数据
response = requests.head('https://jsonplaceholder.typicode.com/posts')
# response.headers 将返回响应头
print(response.headers)
```

### 1.8.3.6 OPTIONS请求

OPTIONS请求一般用于CORS请求，不是所有API都支持。

```python
# content of options_request.py
import requests

# 发出OPTIONS请求，查询服务器支持哪些请求方法
response = requests.options('https://jsonplaceholder.typicode.com/posts')
# 响应头的 'allow' 部分将列出允许的方法
print('Allow:', response.headers.get('allow')) # 也可以检查允许的HTTP方法
```

`CONNECT`和`TRACE`通常用于调试和网络诊断，RESTful web服务通常不实现它们。确保在实际向API发起请求前检查API文档以确认支持的方法。

### 1.8.3.7 响应内容处理

Requests 会自动解码响应内容，并提供一个易于操作的响应对象。

```python
# 响应文本内容
print(response.text)

# 响应字节流
print(response.content)

# JSON响应内容解码为字典
print(response.json())
```

### 1.8.3.8 自定义 Cookies

通过 `cookies` 关键字参数，可以发送带有Cookie的请求。

```python
# content of with_customized_cookie.py
import requests

cookies = {'session_token': '12345'}
response = requests.get('http://httpbin.org/cookies', cookies=cookies)
print(response.text)
```

### 1.8.3.9 自定义header

有时需要自定义HTTP头（headers）来包含额外的信息，如认证令牌、用户代理等，完成业务的特殊API需求。

如果你要发送一个POST请求，并且需要在请求体中发送数据，同时使用自定义头，你可以这样做：

```python
# content of with_customized_headers.py
import requests

url = 'http://httpbin.org/post'
data = {'key': 'value'}
headers = {
    'Authorization': 'Bearer YOUR_ACCESS_TOKEN',
    'Content-Type': 'application/json'
}

response = requests.post(url, json=data, headers=headers)
print(response.text)
```

在这个例子中，我们发送了一个带有JSON数据和自定义头的POST请求。

### 1.8.3.10 会话对象

Requests 可以使用会话（Session）对象来跨请求保持某些参数，例如cookie等。

```python
# content use_session.py
import requests

with requests.Session() as session:
    session.post('http://httpbin.org/post', data={'key': 'value'})
    response = session.get('http://httpbin.org/get')
print(response.text)
```

### 1.8.3.11 异常处理

Python的`requests`库提供了一系列的异常来处理HTTP请求中可能出现的各种问题。以下是`requests`库中常见的异常以及它们的简单示例代码。

#### 1.8.3.11.1 `ConnectTimeout`

当发起HTTP请求，并且希望设定一个连接超时阈值时，可以使用`timeout`参数来指定连接等待的最长时间。如果请求在超时时间内没有成功建立连接，将会抛出一个`requests.exceptions.ConnectTimeout`异常。

```python
# content of connect_timeout.py
import requests
from requests.exceptions import ConnectTimeout

url = 'http://httpbin.org'

try:
    # 发起GET请求并设定连接超时为5秒
    response = requests.get(url, timeout=5)
except ConnectTimeout:
    print(f"请求超时：无法在指定时间内连接到 {url}")
```

#### 1.8.3.11.2 `RequestException`

这是所有Requests异常的基类。

```python
# content of request_exception.py
import requests
from requests.exceptions import RequestException

try:
    response = requests.get('https://httpbin.org/status/404')
    response.raise_for_status()
except RequestException as e:
    print(f'An error occurred: {e}')
```

#### 1.8.3.11.3 `HTTPError`

当HTTP请求返回不成功的状态码时，会抛出此异常。

```python
# content of http_error.py
import requests
from requests.exceptions import HTTPError

try:
    response = requests.get('https://httpbin.org/status/404')
    response.raise_for_status()
except HTTPError as e:
    print(f'HTTP error occurred: {e}')
```

#### 1.8.3.11.4 `ConnectionError`

与网络连接相关的问题，如DNS查询失败、拒绝连接等。

```python
# content of connection_error.py
import requests
from requests.exceptions import ConnectionError

try:
    response = requests.get('http://thisurldoesnotexist.com')
except ConnectionError as e:
    print(f'Connection error occurred: {e}')
```

#### 1.8.3.11.5 `ProxyError`

代理相关的异常。

```python
# content of proxy_error.py
import requests
from requests.exceptions import ProxyError

try:
    proxies = {"http": "http://1.2.3.4:6888"}
    response = requests.get('https://httpbin.org/ip', proxies=proxies)
except ProxyError as e:
    print(f'Proxy error occurred: {e}')
```

#### 1.8.3.11.6 `SSLError`

SSL证书验证失败时抛出此异常。

```python
# content of ssl_error.py
import requests
from requests.exceptions import SSLError

try:
    response = requests.get('https://wrong.host.badssl.com/')
except SSLError as e:
    print(f'SSL error occurred: {e}')
```

#### 1.8.3.11.7 `Timeout`

请求超时异常。

```python
# content of timeout.py
import requests
from requests.exceptions import Timeout

try:
    response = requests.get('https://httpbin.org/delay/5', timeout=2)
except Timeout as e:
    print(f'Timeout error: {e}')
```

#### 1.8.3.11.8 `TooManyRedirects`

请求过多重定向时抛出此异常。

```python
# content of toomanyredirects.py
import requests
from requests.exceptions import TooManyRedirects

# 创建一个Session对象
session = requests.Session()

# 设置最大重定向次数
session.max_redirects = 1

try:
    response = session.get('http://github.com', allow_redirects=True)
except TooManyRedirects as e:
    print(f'Too many redirects: {e}')
```

#### 1.8.3.11.9 `MissingSchema`

当URL缺少HTTP/HTTPS等协议时抛出此异常。

```python
# content of missing_schema.py
import requests
from requests.exceptions import MissingSchema

try:
    response = requests.get('www.google.com')
except MissingSchema as e:
    print(f'Missing URL schema: {e}')
```

#### 1.8.3.11.10 `InvalidURL`

当URL不符合规范时抛出此异常。

```python
# content of invalid_url.py
import requests
from requests.exceptions import InvalidURL

try:
    response = requests.get('http:///httpbin.org')
except InvalidURL as e:
    print(f'Invalid URL: {e}')
```

使用`requests`处理HTTP请求时，理解并正确处理这些异常可以帮助你更好地控制你的网络交互逻辑，并提供更加健壮的错误处理能力。

#### 1.8.3.11.11 `ReadTimeout`

读取超时异常，当读取超时时会抛出该异常。

```python
# content of read_timeout.py
import requests

try:
    response = requests.get("http://httpbin.org", timeout=(0.001, 1))
except requests.exceptions.ReadTimeout as e:
    print("读取超时")
```

#### 1.8.3.11.12 `JSONDecodeError`

JSON解析异常，当返回的内容无法被解析为JSON格式时，会抛出该异常。

```python
# content of json_decode_error.py
import requests

response = requests.get("http://www.baidu.com")
try:
    json_data = response.json()
except requests.exceptions.JSONDecodeError as e:
    print("JSON解析异常")
```

### 1.8.3.12 流式上传

使用 `requests` 发送大文件而无需将其全部加载到内存中：

```python
# content of stream_upload.py
import os
import requests

file_name = 'large_file.txt'

if not os.path.exists(file_name):
    os.system(r"touch {}".format(file_name))

with open(file_name, 'rb') as f:
    response = requests.post('http://httpbin.org/post', data=f)
```

### 1.8.3.13 Basic Auth 认证

对支持 HTTP Basic Auth 的 endpoint 进行认证：

```python
# content of basic_auth.py
import requests

response = requests.get('http://httpbin.org/basic-auth/user/passwd', auth=('user', 'passwd'))
print(response.status_code)
```

也可以使用 `HTTPBasicAuth` 来处理基本的 HTTP 认证：

```python
import requests
from requests.auth import HTTPBasicAuth

response = requests.get('http://httpbin.org/basic-auth/user/passwd', auth=HTTPBasicAuth('user', 'passwd'))
print(response.status_code)
```

### 1.8.3.14 SSL证书验证

Requests 默认验证 SSL 证书，也可以关闭验证或者指定一个自定义证书。

```python
# content of ssl_cert.py
import requests

# 忽略证书验证
response = requests.get('https://httpbin.org/get', verify=False)

# 指定一个本地证书用于客户端认证
response = requests.get('https://httpbin.org/get', cert=('/path/server.crt', '/path/key'))
```

### 1.8.3.15 `hooks`

请求钩子，用于在请求周期内适时调用拦截器。

```python
# content of hooks.py
import requests

hooks = {
    'response': lambda r, *args, **kwargs: print(r.status_code)
}
response = requests.get("http://www.baidu.com", hooks=hooks)
```

### 1.8.3.16 `structures`

`requests`库中，几个重要的数据结构提供了便利的功能，特别针对HTTP请求和响应。以下是这些结构的说明以及用法示例。

#### 1.8.3.16.1 `CaseInsensitiveDict`

这个字典类使得可以忽略HTTP头的大小写，因为按照HTTP RFC 2616标准，HTTP头字段是不区分大小写的。

**用法示例**：

```python
# content of case_in_sensitive_dict.py
import requests
from requests.structures import CaseInsensitiveDict

response = requests.get('https://jsonplaceholder.typicode.com/posts/1')
headers = CaseInsensitiveDict(response.headers)
print(headers['content-type'])
```

#### 1.8.3.16.2 `LookupDict`

`LookupDict`是`requests`库内部使用的一个小型字典类，提供了一些便利的属性对错误码进行快速访问。不过，从`requests` 2.16.0版本开始，`LookupDict` 就被标记为不推荐使用的。我当前使用的是'2.31.0'版本，已经被废弃。

```shell
>>> requests.__version__
'2.31.0'
>>> 
```

#### 1.8.3.16.3 `OrderedDict`

`OrderedDict`是Python标准库`collections`中的一个类，它保持了元素添加的顺序。它特别有用于`requests`中，当需要对参数或者头部信息进行排序时，适用于某些需要按顺序读取KV的特定HTTP服务。

**用法示例**：

```python
# content of ordered_dict.py
from collections import OrderedDict

headers = OrderedDict()
headers['Accept'] = 'application/json'
headers['User-Agent'] = 'my-app/1.0'

print(list(headers.items()))
# 输出: [('Accept', 'application/json'), ('User-Agent', 'my-app/1.0')]
```

在实际的`requests`应用代码中，你更频繁接触到的是`CaseInsensitiveDict`，这是因为处理HTTP响应和请求时经常需要操作headers，而headers就是大小写不敏感的，`LookupDict`已经在新版的`requests`中被移除，`OrderedDict`在requests库内部的确切使用情况较少，但了解其在Python中的用法及特点依旧是有益的。

### 1.8.3.17 Warning

`DependencyWarning`：当requests的依赖库版本无法兼容时，会发出该警告。

```python
# content of dependency_warn.py
import requests
from requests.packages.urllib3.exceptions import DependencyWarning
import warnings

warnings.simplefilter('ignore', DependencyWarning)

response = requests.get("http://www.baidu.com")
print(response.text)
```

`FileModeWarning`：文件打开模式警告，当使用错误的文件打开模式时，会发出该警告。

```python
# content of file_mode_warn.py
import requests
import warnings

warnings.filterwarnings("ignore", category=UserWarning, module='builtins')

with requests.get('http://httpbin.org/stream-bytes/1024',
                  stream=True) as r, open('test.txt', 'wrb') as f:
    for chunk in r.iter_content(chunk_size=1024):
        f.write(chunk)
```

报错信息类似如下：

```shell
ValueError: must have exactly one of create/read/write/append mode
```



## 1.8.4 基于requests实现HTTP请求

构建一个基于Python `requests` 库的封装类为自动化测试框架是一种常见做法，因为它可以简化测试脚本并提高代码的重用性。下面是一个简单的例子来展示如何实现一个基类，来处理HTTP请求的常见操作。

```python
import requests
from requests.exceptions import RequestException

class APIBase(object):
    """API接口基类，封装HTTP请求方法"""

    def __init__(self, base_url):
        """
        初始化方法。
        
        :param base_url: 所有请求的基础URL
        """
        self.base_url = base_url
        self.session = requests.Session()  # 使用session以便跨请求保持一些参数

    def request(self, method, path, data=None, params=None, headers=None, **kwargs):
        """
        发起HTTP请求的通用方法。

        :param method: 请求方法，如'GET', 'POST', 'PUT', 'DELETE'等
        :param path: 请求的URL路径
        :param data: 请求的body数据，字典或字节流
        :param params: URL参数
        :param headers: 请求头
        :param kwargs: 其他传给requests的参数
        :return: Response对象
        """
        url = self.base_url + path
        try:
            response = self.session.request(method=method, url=url, data=data, params=params, headers=headers, **kwargs)
            response.raise_for_status()  # 出现HTTP错误异常时抛出
            return response
        except RequestException as e:
            print(f"请求错误: {e}")

    def get(self, path, **kwargs):
        """
        封装GET请求。

        :param path: 请求的URL路径
        :param kwargs: 传递给通用请求方法的所有参数
        :return: Response对象
        """
        return self.request('GET', path, **kwargs)

    def post(self, path, data=None, json=None, **kwargs):
        """
        封装POST请求。

        :param path: 请求的URL路径
        :param data: Form表单数据
        :param json: JSON请求体
        :param kwargs: 传递给通用请求方法的所有参数
        :return: Response对象
        """
        return self.request('POST', path, data=data, json=json, **kwargs)

    def put(self, path, data=None, **kwargs):
        """
        封装PUT请求。

        :param path: 请求的URL路径
        :param data: 请求的body数据
        :param kwargs: 传递给通用请求方法的所有参数
        :return: Response对象
        """
        return self.request('PUT', path, data=data, **kwargs)

    def delete(self, path, **kwargs):
        """
        封装DELETE请求。

        :param path: 请求的URL路径
        :param kwargs: 传递给通用请求方法的所有参数
        :return: Response对象
        """
        return self.request('DELETE', path, **kwargs)
```

这个基类可以被进一步扩展，比如可以添加错误处理、日志记录、认证、会话管理等更多丰富的特性。这个基类在`pytest`自动化框架中可以作为所有测试用例类的父类，每个测试用例类则为特定的API接口或API组。

使用方法：

```python
# content of test_api.py
from http_request import APIBase

api_base = APIBase("http://httpbin.org")
response = api_base.get("/get")
print(response.status_code)
print(response.text)
```

执行后输出结果：

```shell
root@Gavin:~# python3 test_api.py 
200
{
  "args": {}, 
  "headers": {
    "Accept": "*/*", 
    "Accept-Encoding": "gzip, deflate", 
    "Host": "httpbin.org", 
    "User-Agent": "python-requests/2.31.0", 
    "X-Amzn-Trace-Id": "Root=1-65a0acb4-350ffc2339a4158b513a297e"
  }, 
  "origin": "54.151.130.202", 
  "url": "http://httpbin.org/get"
}

root@Gavin:~#
```



# 1.9 本章小结

本章我们介绍了API（Application Programming Interface）的概念、组成、特点、分类，以及与API相关的Web API、认证与授权，以及Python的requests库。

我们首先了解了API的基本概念，它是一种用于不同软件组件之间进行通信和交互的接口。API的组成包括请求和响应，通过定义和规范化这些接口，不同的应用程序可以相互交互和共享数据。

我们进一步讨论了API的特点，包括抽象、独立性、可组合性和易用性。API的分类涵盖了不同的应用领域，如操作系统API、库API、Web API等，每种API都有其特定的用途和功能。

特别地，我们深入探讨了Web API的概念和使用。Web API是通过HTTP协议进行通信的API，可以用于访问和操作远程服务器上的资源。我们介绍了RESTful API的设计原则和常见的HTTP请求方法，如GET、POST、PUT和DELETE。

另外，我们讨论了API认证与授权的重要性。身份验证用于验证用户的身份，而授权则用于限制和管理用户对资源的访问权限。我们介绍了常见的认证机制，如基本身份验证、令牌验证和OAuth。

最后，我们探索了使用Python的requests库进行API调用的方法和技巧。requests库提供了简单且易用的接口，使我们能够发送HTTP请求、处理响应和处理错误等。

通过本章的学习，我们对API的概念、组成和分类有了更深入的了解。我们了解了Web API的设计原则和常见的认证与授权机制，同时也学习了如何使用Python的requests库进行API调用。
