//
//  APIRequest.swift
//  Music-Driven-Workout-App
//
//  Created by Lucy Newman on 2/27/18.
//  Copyright © 2018 UChicago SoftCon. All rights reserved.
//

import UIKit
import Foundation

class APIRequest: NSObject {
    
    func parseJsonRespone(data: Data) -> [Dictionary<String, Any>]? {
        var res: Dictionary<String, String>
        do {
            res = try JSONSerialization.jsonObject(with: data, options: []) as! Dictionary<String, String>
            let myDict = res
            if let result = myDict["Result"] {
                var reply: [Dictionary<String, Any>]
                
                if let resultData = result.data(using: String.Encoding.utf8) {
                    do {
                        reply = try JSONSerialization.jsonObject(with: resultData, options: []) as! [Dictionary<String, Any>]
                        let myReplyDict = reply
                        return myReplyDict
                    }
                }
            }
            
        } catch let error {
            print(error)
        }
        return nil
    }
    
    
    func submitPostLocal(route: String, qstring: String, completion: @escaping (Data?, URLResponse?,Error?) -> Void) -> URLSessionDataTask {
        var urlComponents = URLComponents()
        urlComponents.scheme = "http"
        urlComponents.host = "127.0.0.1"
        urlComponents.port = 5000
        urlComponents.path = route
        urlComponents.query = qstring
        guard let url = urlComponents.url else {
            fatalError("Could not create URL")
        }
        print("url ", url, "\n")
        
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        let postString = qstring
        request.httpBody = postString.data(using: String.Encoding.utf8)
        print("jsonData: ", String(data: request.httpBody!, encoding: .utf8) ?? "no body data", "\n")
        
        let config = URLSessionConfiguration.default
        let session = URLSession(configuration: config)
        let task = session.dataTask(with: request) {(data, response, responseError) in
            if let data = data {
                completion(data, response, responseError)
            }
        }
        return task
    }

    func submitPostServer(route: String, qstring: String, completion: @escaping (Data?, URLResponse?,Error?) -> Void) -> URLSessionDataTask {
        var urlComponents = URLComponents()
        urlComponents.scheme = "http"
        urlComponents.host = "138.197.49.155"
        urlComponents.port = 8000
        urlComponents.path = route
        urlComponents.query = qstring
        guard let url = urlComponents.url else {
            fatalError("Could not create URL")
        }
        print("url: ", url, "\n")
        
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        let postString = qstring
        request.httpBody = postString.data(using: String.Encoding.utf8)
        
        let config = URLSessionConfiguration.default
        let session = URLSession(configuration: config)
        let task = session.dataTask(with: request) {(data, response, responseError) in
            if let data = data {
                completion(data, response, responseError)
            }
        }
        return task
    }
    
}
