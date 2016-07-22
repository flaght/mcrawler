1. 本插件实现从crawler_cookie数据库中读取：
	int64 attr_id;
	string cookie;
	string last_time;
	
2. 等待require_cookie进入，require包：
	struct RequireLoginCookie: public PacketHead {
	int32 manage_id;
	char token[32];
	int64 attr_id;
	int8 amount;
};

3. 打包发送cookie：
struct LoginCookieSet: public PacketHead {
	int64 attri_id;	
	int32 len;
	std::list<LoginCookieUnit*> login_cookie_set;
};

struct LoginCookieUnit {
	std::string login_cookie_body;
	std::string login_last_time;
};