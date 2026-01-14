package com.aegisops.api;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.web.servlet.FilterRegistrationBean;
import org.springframework.context.annotation.Bean;
import com.aegisops.api.security.SecurityConfig;


@SpringBootApplication
public class ApiApplication {
    public static void main(String[] args) {
        SpringApplication.run(ApiApplication.class, args);
    }
BROKEN_CODE_HERE

    @Bean
    public FilterRegistrationBean<SecurityConfig> securityFilter(SecurityConfig securityConfig) {
        FilterRegistrationBean<SecurityConfig> bean = new FilterRegistrationBean<>();
        bean.setFilter(securityConfig);
        bean.addUrlPatterns("/*"); // protect all routes
        return bean;
    }

}