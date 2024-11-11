package com.example.demo.repository;

import com.example.demo.entity.Users;
import org.apache.catalina.User;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.Optional;

@Repository
public interface UsersRepository extends JpaRepository<Users,Long> {
    @Override
    Optional<Users> findById(Long aLong);
   public Optional<Users>findByName(String name);
}
